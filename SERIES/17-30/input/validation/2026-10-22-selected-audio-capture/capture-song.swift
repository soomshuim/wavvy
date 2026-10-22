import AVFoundation
import AudioToolbox
import CoreGraphics
import Foundation
import ScreenCaptureKit

final class AudioSink: NSObject, SCStreamOutput, SCStreamDelegate {
    let queue = DispatchQueue(label: "wavvy.screen-capture-audio")
    private var file: AVAudioFile?
    private(set) var buffers = 0
    private(set) var frames = 0
    private(set) var writeError: String?
    private(set) var rawPeak: Double = 0
    private(set) var rawSquaredSum: Double = 0
    private(set) var rawSamples = 0
    private(set) var rawNonzeroBytes = 0
    private(set) var rawBytes = 0
    private(set) var rawFormat = "unknown"

    init(url: URL) throws {
        let settings: [String: Any] = [
            AVFormatIDKey: kAudioFormatLinearPCM,
            AVSampleRateKey: 48_000,
            AVNumberOfChannelsKey: 2,
            AVLinearPCMBitDepthKey: 32,
            AVLinearPCMIsFloatKey: true,
            AVLinearPCMIsNonInterleaved: true,
        ]
        file = try AVAudioFile(
            forWriting: url,
            settings: settings,
            commonFormat: .pcmFormatFloat32,
            interleaved: false
        )
    }

    func stream(
        _ stream: SCStream,
        didOutputSampleBuffer sampleBuffer: CMSampleBuffer,
        of type: SCStreamOutputType
    ) {
        guard type == .audio, CMSampleBufferIsValid(sampleBuffer),
              CMSampleBufferDataIsReady(sampleBuffer) else { return }
        do {
            try sampleBuffer.withAudioBufferList { audioBufferList, _ in
                guard let description = sampleBuffer.formatDescription?.audioStreamBasicDescription,
                      let format = AVAudioFormat(
                        standardFormatWithSampleRate: description.mSampleRate,
                        channels: description.mChannelsPerFrame
                      ),
                      let pcm = AVAudioPCMBuffer(
                        pcmFormat: format,
                        bufferListNoCopy: audioBufferList.unsafePointer
                      ) else { return }
                if rawFormat == "unknown" {
                    rawFormat = "formatID=\(description.mFormatID) flags=\(description.mFormatFlags) bits=\(description.mBitsPerChannel) channels=\(description.mChannelsPerFrame) sampleRate=\(description.mSampleRate)"
                }
                let buffer = audioBufferList.unsafePointer.pointee.mBuffers
                if let data = buffer.mData {
                    let byteCount = Int(buffer.mDataByteSize)
                    rawBytes += byteCount
                    let bytes = data.bindMemory(to: UInt8.self, capacity: byteCount)
                    for i in 0..<byteCount where bytes[i] != 0 { rawNonzeroBytes += 1 }
                    if description.mBitsPerChannel == 32 && (description.mFormatFlags & kAudioFormatFlagIsFloat) != 0 {
                        let count = byteCount / MemoryLayout<Float>.size
                        let values = data.bindMemory(to: Float.self, capacity: count)
                        for i in 0..<count {
                            let value = Double(values[i])
                            if value.isFinite {
                                rawPeak = max(rawPeak, abs(value))
                                rawSquaredSum += value * value
                                rawSamples += 1
                            }
                        }
                    } else if description.mBitsPerChannel == 16 && (description.mFormatFlags & kAudioFormatFlagIsSignedInteger) != 0 {
                        let count = byteCount / MemoryLayout<Int16>.size
                        let values = data.bindMemory(to: Int16.self, capacity: count)
                        for i in 0..<count {
                            let value = Double(values[i]) / 32768
                            rawPeak = max(rawPeak, abs(value))
                            rawSquaredSum += value * value
                            rawSamples += 1
                        }
                    }
                }
                pcm.frameLength = AVAudioFrameCount(CMSampleBufferGetNumSamples(sampleBuffer))
                try file?.write(from: pcm)
                buffers += 1
                frames += Int(pcm.frameLength)
            }
        } catch {
            writeError = String(describing: error)
        }
    }

    func finish() {
        queue.sync { file = nil }
    }
}

@main
struct CaptureTest {
    static func main() async {
        let args = CommandLine.arguments
        guard args.count >= 2 else {
            fputs("usage: capture preflight|request|list|record <Aside pid> <max-seconds> <output.wav> <stop-marker>\n", stderr)
            exit(2)
        }
        if args[1] == "preflight" {
            print("screen_recording_preflight=\(CGPreflightScreenCaptureAccess())")
            return
        }
        if args[1] == "request" {
            print("screen_recording_request=\(CGRequestScreenCaptureAccess())")
            return
        }
        guard CGPreflightScreenCaptureAccess() else {
            fputs("Screen Recording permission is not granted to this process.\n", stderr)
            exit(3)
        }
        do {
            let content = try await SCShareableContent.excludingDesktopWindows(
                false,
                onScreenWindowsOnly: args[1] == "list-onscreen"
            )
            if args[1] == "list" || args[1] == "list-onscreen" {
                print("displays=\(content.displays.count) apps=\(content.applications.count) windows=\(content.windows.count)")
                for app in content.applications {
                    print("app pid=\(app.processID) bundle=\(app.bundleIdentifier) name=\(app.applicationName)")
                }
                for window in content.windows {
                    print("window id=\(window.windowID) pid=\(window.owningApplication!.processID) title=\(window.title ?? "")")
                }
                return
            }
            guard args[1] == "record", args.count == 6,
                  let pid = Int32(args[2]), let seconds = UInt64(args[3]),
                  seconds > 0, seconds <= 360 else {
                fputs("record arguments invalid\n", stderr)
                exit(2)
            }
            let matched = content.applications.filter { $0.processID == pid }
            guard matched.count == 1,
                  matched[0].applicationName.localizedCaseInsensitiveContains("Aside") else {
                fputs("target app pid is not uniquely Aside\n", stderr)
                exit(4)
            }
            guard let display = content.displays.first(where: { $0.displayID == CGMainDisplayID() }) else {
                fputs("main display not shareable\n", stderr)
                exit(4)
            }
            let output = URL(fileURLWithPath: args[4])
            let stopMarker = URL(fileURLWithPath: args[5])
            guard !FileManager.default.fileExists(atPath: output.path) else {
                fputs("output already exists\n", stderr)
                exit(4)
            }
            guard !FileManager.default.fileExists(atPath: stopMarker.path) else {
                fputs("stop marker already exists\n", stderr)
                exit(4)
            }
            let filter = SCContentFilter(display: display, including: matched, exceptingWindows: [])
            let configuration = SCStreamConfiguration()
            configuration.capturesAudio = true
            configuration.captureMicrophone = false
            configuration.sampleRate = 48_000
            configuration.channelCount = 2
            configuration.excludesCurrentProcessAudio = true
            configuration.width = 2
            configuration.height = 2
            configuration.minimumFrameInterval = CMTime(value: 1, timescale: 1)
            let sink = try AudioSink(url: output)
            let stream = SCStream(filter: filter, configuration: configuration, delegate: sink)
            try stream.addStreamOutput(sink, type: .audio, sampleHandlerQueue: sink.queue)
            try await stream.startCapture()
            print("capture_started pid=\(pid) app=\(matched[0].applicationName) bundle=\(matched[0].bundleIdentifier) microphone=false audio=true output=\(output.path) stop_marker=\(stopMarker.path) max_seconds=\(seconds)")
            fflush(stdout)
            let deadline = Date().addingTimeInterval(TimeInterval(seconds))
            var stopReason = "max_duration"
            while Date() < deadline {
                if FileManager.default.fileExists(atPath: stopMarker.path) {
                    stopReason = "stop_marker"
                    break
                }
                try await Task.sleep(nanoseconds: 100_000_000)
            }
            try await stream.stopCapture()
            sink.finish()
            let rawRMS = sink.rawSamples > 0 ? sqrt(sink.rawSquaredSum / Double(sink.rawSamples)) : 0
            print("capture_stopped reason=\(stopReason) buffers=\(sink.buffers) frames=\(sink.frames) write_error=\(sink.writeError ?? "none") raw_format=\(sink.rawFormat) raw_peak=\(sink.rawPeak) raw_rms=\(rawRMS) raw_samples=\(sink.rawSamples) raw_nonzero_bytes=\(sink.rawNonzeroBytes) raw_bytes=\(sink.rawBytes)")
            if sink.buffers == 0 || sink.writeError != nil { exit(5) }
        } catch {
            fputs("capture_error=\(error)\n", stderr)
            exit(6)
        }
    }
}
