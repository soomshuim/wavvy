import Foundation
import CoreGraphics
import CoreText
import ImageIO
import CryptoKit

// One-off compositor for the user's explicitly selected local-overlay method.
// The decoded source RGB samples are copied; only nonzero overlay-alpha pixels change.
let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let sourceURL = root.appendingPathComponent("SERIES/06-30/input/thumbnail-draft-runningwear-tiedhair-20261024.png")
let logoURL = root.appendingPathComponent("brand/logo_wavvy.png")
let outputURL = root.appendingPathComponent("SERIES/06-30/input/thumbnail-branded-0630-20261024.png")
let overlayURL = root.appendingPathComponent("work/thumbnail-flat-white-overlay-20261024.png")
let sourceSHA = "3a8a528e99d87d1a202a29baddc50bf04e791d170e5d15a3522f8cf03898404d"

func require(_ ok: @autoclosure () -> Bool, _ message: String) {
    if !ok() { fputs("ERROR: \(message)\n", stderr); exit(1) }
}
func sha(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }
func image(_ data: Data) -> CGImage {
    guard let s = CGImageSourceCreateWithData(data as CFData, nil), let i = CGImageSourceCreateImageAtIndex(s, 0, nil) else { fatalError("Cannot decode image") }
    return i
}
func samples(_ image: CGImage) -> [UInt8] {
    guard let d = image.dataProvider?.data else { fatalError("Missing decoded samples") }
    return Array(UnsafeBufferPointer(start: CFDataGetBytePtr(d), count: CFDataGetLength(d)))
}
func png(_ image: CGImage) -> Data {
    let d = NSMutableData()
    guard let dst = CGImageDestinationCreateWithData(d, "public.png" as CFString, 1, nil) else { fatalError("Cannot create PNG encoder") }
    CGImageDestinationAddImage(dst, image, nil)
    require(CGImageDestinationFinalize(dst), "PNG encoder failed")
    return d as Data
}
struct PNGChunk { let name: String; let raw: Data }
let colorChunks: Set<String> = ["cHRM", "gAMA", "iCCP", "sRGB", "cICP", "mDCV", "cLLI"]
func chunks(_ data: Data) -> [PNGChunk] {
    require(data.prefix(8) == Data([137,80,78,71,13,10,26,10]), "Not a PNG")
    var out: [PNGChunk] = []; var offset = 8
    while offset + 12 <= data.count {
        let n = data[offset..<(offset+4)].reduce(0) { ($0 << 8) | Int($1) }
        require(n <= data.count - offset - 12, "Invalid PNG chunk length")
        let name = String(bytes: data[(offset+4)..<(offset+8)], encoding: .ascii)!
        out.append(PNGChunk(name: name, raw: data.subdata(in: offset..<(offset+n+12))))
        offset += n + 12
        if name == "IEND" { break }
    }
    require(offset == data.count, "Unexpected trailing PNG data")
    return out
}
func preservingSourceColorChunks(_ encoded: Data, source: Data) -> Data {
    let src = chunks(source).filter { colorChunks.contains($0.name) }
    let dst = chunks(encoded)
    require(dst.first?.name == "IHDR", "Missing output IHDR")
    var d = encoded.prefix(8)
    d.append(dst[0].raw)
    for c in src { d.append(c.raw) }
    for c in dst.dropFirst() where !colorChunks.contains(c.name) { d.append(c.raw) }
    return Data(d)
}
func colorChunkReport(_ data: Data) -> [[String: Any]] {
    chunks(data).filter { colorChunks.contains($0.name) }.map { ["type": $0.name, "bytes": $0.raw.count, "sha256": sha($0.raw)] }
}

let sourceData = try Data(contentsOf: sourceURL)
require(sha(sourceData) == sourceSHA, "Selected photo changed")
require(!chunks(sourceData).contains(where: { $0.name == "iCCP" }), "Expected the inspected source without an embedded ICC profile")
let base = image(sourceData)
require(base.width == 1672 && base.height == 941, "Unexpected photo dimensions")
require(base.bitsPerComponent == 8 && base.bitsPerPixel == 32 && base.alphaInfo == .noneSkipLast && base.bitmapInfo.intersection(.byteOrderMask).isEmpty, "Expected the inspected opaque 8-bit RGBX source format")
guard let sourceColorSpace = base.colorSpace else { fatalError("Missing source color space") }
let width = base.width; let height = base.height; let row = width * 4
require(base.bytesPerRow == row, "Unexpected source row stride")
let baseBytes = samples(base)
let logo = image(try Data(contentsOf: logoURL))

var fontReports: [[String: Any]] = []
func exactFont(path: String, postScriptName: String, size: CGFloat) -> CTFont {
    let url = URL(fileURLWithPath: path)
    require(FileManager.default.fileExists(atPath: path), "Exact font file missing: \(path)")
    var error: Unmanaged<CFError>?
    let registered = CTFontManagerRegisterFontsForURL(url as CFURL, .process, &error)
    let registrationError = error?.takeRetainedValue()
    guard let descriptors = CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
          let descriptor = descriptors.first(where: { CTFontDescriptorCopyAttribute($0, kCTFontNameAttribute) as? String == postScriptName }) else { fatalError("Exact face missing from font file: \(postScriptName)") }
    let font = CTFontCreateWithFontDescriptor(descriptor, size, nil)
    require(CTFontCopyPostScriptName(font) as String == postScriptName, "Font substitution detected")
    guard let resolved = CTFontCopyAttribute(font, kCTFontURLAttribute) as? URL else { fatalError("Cannot verify font URL") }
    require(resolved.resolvingSymlinksInPath() == url.resolvingSymlinksInPath(), "Resolved font came from another file")
    fontReports.append(["file": path, "file_sha256": sha(try! Data(contentsOf: url)), "postscript_name": postScriptName, "point_size": size, "resolved_file": resolved.path, "process_registration_succeeded": registered, "registration_error": registrationError.map { String(describing: $0) } ?? "none", "fallback": false])
    return font
}
let cadenceFont = exactFont(path: "/Library/Fonts/SF-Pro-Display-Thin.otf", postScriptName: "SFProDisplay-Thin", size: 50)
let tempoFont = exactFont(path: "/System/Library/Fonts/HelveticaNeue.ttc", postScriptName: "HelveticaNeue-CondensedBlack", size: 148)

var overlay = [UInt8](repeating: 0, count: row * height)
var layers: [[String: Any]] = []
let white = CGColor(colorSpace: sourceColorSpace, components: [1,1,1,1])!
overlay.withUnsafeMutableBytes { bytes in
    guard let ctx = CGContext(data: bytes.baseAddress, width: width, height: height, bitsPerComponent: 8, bytesPerRow: row, space: sourceColorSpace, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Big.rawValue) else { fatalError("Cannot create transparent overlay") }
    ctx.setShadow(offset: .zero, blur: 0, color: nil)
    ctx.setBlendMode(.normal)
    ctx.setShouldAntialias(true)
    ctx.setShouldSmoothFonts(false)
    ctx.setFillColor(white)
    ctx.setStrokeColor(white)
    // Quartz's bottom-left coordinate system; all reported layout values are top-left.
    let logoHeight = CGFloat(logo.height) * 284 / CGFloat(logo.width)
    let logoRect = CGRect(x: 65, y: CGFloat(height) - 56 - logoHeight, width: 284, height: logoHeight)
    ctx.saveGState()
    ctx.clip(to: logoRect, mask: logo)
    ctx.fill(logoRect)
    ctx.restoreGState()
    layers.append(["kind": "real_brand_logo_alpha", "source": "brand/logo_wavvy.png", "layout_rect_xywh": [65.0,56.0,284.0,Double(logoHeight)]])
    func text(_ string: String, font: CTFont, left: CGFloat, visibleTop: CGFloat) {
        let line = CTLineCreateWithAttributedString(NSAttributedString(string: string, attributes: [NSAttributedString.Key(kCTFontAttributeName as String): font, NSAttributedString.Key(kCTForegroundColorAttributeName as String): white]))
        let bounds = CTLineGetImageBounds(line, nil)
        for run in CTLineGetGlyphRuns(line) as! [CTRun] {
            let attrs = CTRunGetAttributes(run) as NSDictionary
            let actual = attrs[kCTFontAttributeName] as! CTFont
            require(CTFontCopyPostScriptName(actual) as String == CTFontCopyPostScriptName(font) as String, "Glyph fallback detected")
        }
        let baseline = CGPoint(x: left - bounds.minX, y: CGFloat(height) - visibleTop - bounds.maxY)
        ctx.textMatrix = .identity
        ctx.textPosition = baseline
        CTLineDraw(line, ctx)
        layers.append(["kind": "text", "text": string, "postscript_name": CTFontCopyPostScriptName(font) as String, "font_size": CTFontGetSize(font), "visible_bounds_xywh": [Double(left),Double(visibleTop),Double(bounds.width),Double(bounds.height)], "baseline_quartz_xy": [Double(baseline.x),Double(baseline.y)]])
    }
    text("Cadence", font: cadenceFont, left: 64, visibleTop: 689)
    ctx.setLineWidth(1)
    ctx.setLineCap(.butt)
    ctx.move(to: CGPoint(x: 261, y: CGFloat(height) - 718.5))
    ctx.addLine(to: CGPoint(x: 600, y: CGFloat(height) - 718.5))
    ctx.strokePath()
    layers.append(["kind": "horizontal_line", "from_top_left_xy": [261,718.5], "to_top_left_xy": [600,718.5], "width": 1])
    text("175 BPM", font: tempoFont, left: 64, visibleTop: 755)
}

var finalBytes = baseBytes
var maskPixels = 0; var changedInside = 0
for pixel in 0..<(width*height) {
    let i = pixel*4; let alpha = Int(overlay[i+3])
    if alpha == 0 { continue }
    maskPixels += 1
    var changed = false
    for c in 0..<3 {
        let value = UInt8((Int(baseBytes[i+c]) * (255-alpha) + 255*alpha + 127) / 255)
        changed = changed || value != baseBytes[i+c]
        finalBytes[i+c] = value
    }
    if changed { changedInside += 1 }
}
func cgImage(_ bytes: [UInt8], alpha: CGImageAlphaInfo) -> CGImage {
    let d = Data(bytes)
    return CGImage(width: width, height: height, bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: row, space: sourceColorSpace, bitmapInfo: CGBitmapInfo(rawValue: alpha.rawValue | CGBitmapInfo.byteOrder32Big.rawValue), provider: CGDataProvider(data: d as CFData)!, decode: nil, shouldInterpolate: false, intent: .defaultIntent)!
}
let encoded = preservingSourceColorChunks(png(cgImage(finalBytes, alpha: .noneSkipLast)), source: sourceData)
let decoded = image(encoded)
require(decoded.bitsPerPixel == 32 && decoded.bitsPerComponent == 8 && decoded.bytesPerRow == row && decoded.alphaInfo == .noneSkipLast, "Unexpected final PNG decode format")
require(decoded.colorSpace?.name == base.colorSpace?.name, "PNG color-space identity changed")
require((decoded.colorSpace?.copyICCData() as Data?) == (base.colorSpace?.copyICCData() as Data?), "CoreGraphics-resolved color-space data changed")
require(colorChunkReport(encoded).map { $0["sha256"] as! String } == colorChunkReport(sourceData).map { $0["sha256"] as! String }, "PNG color metadata changed")
let decodedBytes = samples(decoded)
var outsideDifferences = 0; var allOutsideRGBChannelDifferences = 0
for pixel in 0..<(width*height) where overlay[pixel*4+3] == 0 {
    let i = pixel*4
    if (0..<3).contains(where: { decodedBytes[i+$0] != baseBytes[i+$0] }) { outsideDifferences += 1 }
    for c in 0..<3 where decodedBytes[i+c] != baseBytes[i+c] { allOutsideRGBChannelDifferences += 1 }
}
require(outsideDifferences == 0, "Photo changed outside overlay alpha")
// Save the exact alpha layer temporarily for the controller's independent check.
let overlayData = png(cgImage(overlay, alpha: .premultipliedLast))
try FileManager.default.createDirectory(at: overlayURL.deletingLastPathComponent(), withIntermediateDirectories: true)
try overlayData.write(to: overlayURL, options: .atomic)
try encoded.write(to: outputURL, options: .atomic)
let report: [String: Any] = [
    "method": "local_composite", "user_selection": "원본 사진에 글자만 합성해줘 (추천)", "tool": "Swift / CoreGraphics / CoreText / ImageIO",
    // copyICCData() describes CoreGraphics' resolved sRGB color space; these PNGs contain no iCCP chunk.
    "source": ["path": sourceURL.path, "sha256": sourceSHA, "dimensions": [width,height], "coregraphics_resolved_color_space": String(describing: base.colorSpace?.name), "coregraphics_resolved_icc_sha256": (base.colorSpace?.copyICCData() as Data?).map(sha) ?? "absent", "embedded_icc_present": false, "embedded_icc_bytes": 0, "embedded_icc_sha256": sha(Data()), "color_chunks": colorChunkReport(sourceData)],
    "output": ["path": outputURL.path, "sha256": sha(encoded), "bytes": encoded.count, "dimensions": [width,height], "coregraphics_resolved_color_space": String(describing: decoded.colorSpace?.name), "coregraphics_resolved_icc_sha256": (decoded.colorSpace?.copyICCData() as Data?).map(sha) ?? "absent", "embedded_icc_present": false, "embedded_icc_bytes": 0, "embedded_icc_sha256": sha(Data()), "color_chunks": colorChunkReport(encoded)],
    "fonts": fontReports, "layers": layers, "exact_text": ["Wavvy","Cadence","175 BPM"], "time": false, "shadow": false, "glow": false, "outline": false, "photo_adjustments": false,
    "verification": ["overlay_nonzero_alpha_pixels": maskPixels, "changed_pixels_inside_overlay": changedInside, "outside_overlay_pixels": width*height-maskPixels, "outside_overlay_different_rgb_pixels": outsideDifferences, "outside_overlay_different_rgb_channels": allOutsideRGBChannelDifferences, "coregraphics_resolved_color_space_equal": true, "embedded_icc_presence_equal": true, "embedded_icc_present_in_either_png": false, "source_color_chunks_copied_byte_for_byte": true],
    "temporary_exact_overlay": ["path": overlayURL.path, "sha256": sha(overlayData), "bytes": overlayData.count, "controller_deletion_pending": true]
]
print(String(data: try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted,.sortedKeys]), encoding: .utf8)!)
