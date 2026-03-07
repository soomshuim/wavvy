#!/usr/bin/env python3
"""
vibem - YouTube Music Playlist Generation CLI

A robust CLI tool for automating YouTube music playlist generation
using pure FFmpeg for all media operations.

Author: vibem
License: MIT
"""

import click
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import ffmpeg
import pandas as pd


# =============================================================================
# CONSTANTS
# =============================================================================

TRACK_PATTERN = re.compile(
    r'^(?P<order>\d{2})__(?P<title>[^_]+)__(?P<mood>[^_]+)__(?P<genre>[^_]+)__(?P<bpm>\d+)\.(?:mp3|wav)$'
)

DEFAULT_CROSSFADE_SEC = 0.8
DEFAULT_LUFS = -14
DEFAULT_TRUE_PEAK = -1.0
DEFAULT_PREVIEW_SEC = 30

VIDEO_CODEC = 'libx264'
AUDIO_CODEC = 'aac'
AUDIO_BITRATE = '320k'
VIDEO_CRF = 18
VIDEO_PRESET = 'medium'

# FFmpeg binary paths (ffmpeg-full has drawtext support)
FFMPEG_FULL_PATH = '/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg'
FFMPEG_DEFAULT = 'ffmpeg'


def get_ffmpeg_binary(needs_drawtext: bool = False) -> str:
    """
    Get the appropriate FFmpeg binary path.
    Uses ffmpeg-full when drawtext filter is needed (for text overlays).
    """
    if needs_drawtext and Path(FFMPEG_FULL_PATH).exists():
        return FFMPEG_FULL_PATH
    return FFMPEG_DEFAULT


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TrackInfo:
    """Parsed track information from filename."""
    path: Path
    order: int
    title: str
    mood: str
    genre: str
    bpm: int
    duration: float = 0.0
    sample_rate: int = 0
    sha256: str = ""

    @classmethod
    def from_filename(cls, path: Path) -> Optional['TrackInfo']:
        """Parse track info from filename. Returns None if invalid."""
        match = TRACK_PATTERN.match(path.name)
        if not match:
            return None
        return cls(
            path=path,
            order=int(match.group('order')),
            title=match.group('title'),
            mood=match.group('mood'),
            genre=match.group('genre'),
            bpm=int(match.group('bpm')),
        )


@dataclass
class ValidationResult:
    """Result of validation checks."""
    is_valid: bool = True
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    tracks: list = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.is_valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def log_info(msg: str):
    """Print info message."""
    click.echo(click.style(f"[INFO] {msg}", fg='blue'))


def log_success(msg: str):
    """Print success message."""
    click.echo(click.style(f"[OK] {msg}", fg='green'))


def log_warning(msg: str):
    """Print warning message."""
    click.echo(click.style(f"[WARN] {msg}", fg='yellow'))


def log_error(msg: str):
    """Print error message."""
    click.echo(click.style(f"[ERROR] {msg}", fg='red'), err=True)


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_audio_info(filepath: Path) -> dict:
    """Get audio file info using ffprobe."""
    try:
        probe = ffmpeg.probe(str(filepath))
        audio_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'audio'),
            None
        )
        if not audio_stream:
            return {'error': 'No audio stream found'}

        duration = float(probe['format'].get('duration', 0))
        sample_rate = int(audio_stream.get('sample_rate', 0))

        return {
            'duration': duration,
            'sample_rate': sample_rate,
            'codec': audio_stream.get('codec_name', 'unknown'),
            'channels': audio_stream.get('channels', 0),
            'bit_rate': probe['format'].get('bit_rate', 'unknown'),
        }
    except ffmpeg.Error as e:
        return {'error': f'ffprobe failed: {e.stderr.decode() if e.stderr else str(e)}'}
    except Exception as e:
        return {'error': str(e)}


def get_video_info(filepath: Path) -> dict:
    """Get video file info using ffprobe."""
    try:
        probe = ffmpeg.probe(str(filepath))
        video_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'video'),
            None
        )
        if not video_stream:
            return {'error': 'No video stream found'}

        duration = float(probe['format'].get('duration', 0))

        return {
            'duration': duration,
            'width': video_stream.get('width', 0),
            'height': video_stream.get('height', 0),
            'codec': video_stream.get('codec_name', 'unknown'),
        }
    except ffmpeg.Error as e:
        return {'error': f'ffprobe failed: {e.stderr.decode() if e.stderr else str(e)}'}
    except Exception as e:
        return {'error': str(e)}


# =============================================================================
# FONT AND TEXT OVERLAY
# =============================================================================

def get_system_font_path() -> Optional[str]:
    """
    Get system font path for Korean text rendering.
    Returns None if no suitable font is found.
    """
    import platform

    system = platform.system()

    # macOS font paths
    if system == 'Darwin':
        font_candidates = [
            '/System/Library/Fonts/AppleSDGothicNeo.ttc',
            '/Library/Fonts/AppleGothic.ttf',
            '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
        ]
    # Linux font paths
    elif system == 'Linux':
        font_candidates = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        ]
    # Windows font paths
    elif system == 'Windows':
        font_candidates = [
            'C:/Windows/Fonts/malgun.ttf',
            'C:/Windows/Fonts/gulim.ttc',
        ]
    else:
        font_candidates = []

    for font_path in font_candidates:
        if Path(font_path).exists():
            return font_path

    return None


def get_pretendard_font_path(weight: str = "Medium") -> Optional[str]:
    """Get Pretendard font path by weight.

    Available weights: Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, Black
    """
    home = Path.home()
    font_dirs = [
        home / "Library/Fonts",  # macOS user fonts
        Path("/Library/Fonts"),  # macOS system fonts
        Path("/usr/share/fonts/truetype/pretendard"),  # Linux
    ]

    for font_dir in font_dirs:
        font_path = font_dir / f"Pretendard-{weight}.otf"
        if font_path.exists():
            return str(font_path)
        # Try ttf variant
        font_path = font_dir / f"Pretendard-{weight}.ttf"
        if font_path.exists():
            return str(font_path)

    return None


# Default fonts for Shorts (lazy loaded to avoid startup overhead)
_SHORTS_TITLE_FONT: Optional[str] = None
_SHORTS_LYRIC_FONT: Optional[str] = None


def get_shorts_title_font() -> Optional[str]:
    """Get default title font (Pretendard Black)."""
    global _SHORTS_TITLE_FONT
    if _SHORTS_TITLE_FONT is None:
        _SHORTS_TITLE_FONT = get_pretendard_font_path("Black")
    return _SHORTS_TITLE_FONT


def get_shorts_lyric_font() -> Optional[str]:
    """Get default lyric font (Pretendard Medium)."""
    global _SHORTS_LYRIC_FONT
    if _SHORTS_LYRIC_FONT is None:
        _SHORTS_LYRIC_FONT = get_pretendard_font_path("Medium")
    return _SHORTS_LYRIC_FONT


def escape_ffmpeg_text(text: str) -> str:
    """Escape special characters for FFmpeg drawtext filter."""
    # FFmpeg drawtext requires escaping: \ ' :
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace(':', '\\:')
    return text


def build_text_overlay_filter(
    title: Optional[str] = None,
    title_duration: float = 4.0,
    lyric: Optional[str] = None,
    lyric_delay: float = 1.0,
    title_font_path: Optional[str] = None,
    lyric_font_path: Optional[str] = None,
    title_fontsize: int = 48,
    lyric_fontsize: int = 28,
) -> Optional[str]:
    """
    Build FFmpeg filter string for 2-layer text overlay.

    Layer 1 (Title): Center (45%), appears 0-2s, fades out 2-4s
    Layer 2 (Lyric): Lower center (62.5%), fades in after delay, stays until end

    Default fonts:
    - Title: Pretendard Black (Heavy)
    - Lyric: Pretendard Medium

    Returns None if no text is provided.
    """
    if not title and not lyric:
        return None

    # Get font paths with Pretendard defaults
    if not title_font_path:
        title_font_path = get_shorts_title_font() or get_system_font_path()
    if not lyric_font_path:
        lyric_font_path = get_shorts_lyric_font() or get_system_font_path()

    # Fallback to FFmpeg default
    if not title_font_path:
        log_warning("No title font found. Text overlay may not render correctly.")
        title_font_path = "sans"
    if not lyric_font_path:
        log_warning("No lyric font found. Text overlay may not render correctly.")
        lyric_font_path = "sans"

    filters = []

    # Title filter (center, fade out)
    if title:
        escaped_title = escape_ffmpeg_text(title)
        fade_start = title_duration / 2
        fade_duration = title_duration / 2

        title_filter = (
            f"drawtext=text='{escaped_title}':"
            f"fontfile='{title_font_path}':"
            f"fontsize={title_fontsize}:"
            f"fontcolor=white:"
            f"x=(w-text_w)/2:"
            f"y=h*0.45-text_h/2:"
            f"enable='between(t,0,{title_duration})':"
            f"alpha='if(lt(t,{fade_start}),1,max(0,1-(t-{fade_start})/{fade_duration}))'"
        )
        filters.append(title_filter)

    # Lyric filter (lower center, fade in then stay)
    if lyric:
        escaped_lyric = escape_ffmpeg_text(lyric)

        lyric_filter = (
            f"drawtext=text='{escaped_lyric}':"
            f"fontfile='{lyric_font_path}':"
            f"fontsize={lyric_fontsize}:"
            f"fontcolor=white:"
            f"x=(w-text_w)/2:"
            f"y=h*0.625-text_h/2:"
            f"alpha='if(lt(t,{lyric_delay}),0,min(1,(t-{lyric_delay})/1))'"
        )
        filters.append(lyric_filter)

    return ",".join(filters)


# =============================================================================
# PATH RESOLVER
# =============================================================================

class ProjectPaths:
    """Resolve and manage project paths."""

    def __init__(self, base_path: Path):
        self.base = base_path
        self.input_dir = base_path / 'input'
        self.tracks_dir = self.input_dir / 'tracks'
        self.work_dir = base_path / 'work'
        self.output_dir = base_path / 'output'
        self.norm_tracks_dir = self.work_dir / 'norm_tracks'

        # Input files
        self.loop_video = self.input_dir / 'loop.mp4'
        self.loop_xfade = self.input_dir / 'loop_xfade.mp4'
        self.loop_xfade_test = self.input_dir / 'loop_xfade_test.mp4'
        self.thumbnail = self.input_dir / 'thumb.jpg'

        # Work files
        self.merged_wav = self.work_dir / 'merged.wav'

        # Output files
        self.preview_mp4 = self.output_dir / 'preview.mp4'
        self.final_mp4 = self.output_dir / 'final.mp4'
        self.provenance_md = self.output_dir / 'provenance.md'
        self.draft_description = self.output_dir / 'draft_description.txt'
        self.upload_csv = self.output_dir / 'upload.csv'
        self.report_json = self.output_dir / 'report.json'

    def ensure_work_dirs(self):
        """Create work and output directories."""
        ensure_dir(self.work_dir)
        ensure_dir(self.norm_tracks_dir)
        ensure_dir(self.output_dir)

    def clean_work_dir(self):
        """Clean work directory."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)
        ensure_dir(self.work_dir)
        ensure_dir(self.norm_tracks_dir)


# =============================================================================
# VALIDATION
# =============================================================================

def validate_project(paths: ProjectPaths) -> ValidationResult:
    """
    Validate project structure and files.

    Checks:
    1. tracks/ contains at least one MP3
    2. Filename format matches spec (NN__Title__Mood__Genre__BPM.mp3)
    3. loop.mp4 and thumb.jpg exist
    4. Audio integrity via ffprobe
    5. Sample rate consistency
    """
    result = ValidationResult()

    # Check base directory exists
    if not paths.base.exists():
        result.add_error(f"Project directory does not exist: {paths.base}")
        return result

    # Check input directory structure
    if not paths.input_dir.exists():
        result.add_error(f"Input directory does not exist: {paths.input_dir}")
        return result

    if not paths.tracks_dir.exists():
        result.add_error(f"Tracks directory does not exist: {paths.tracks_dir}")
        return result

    # Find audio files (MP3 or WAV)
    audio_files = sorted(
        list(paths.tracks_dir.glob('*.mp3')) + list(paths.tracks_dir.glob('*.wav'))
    )
    if not audio_files:
        result.add_error(f"No audio files (MP3/WAV) found in: {paths.tracks_dir}")
        return result

    log_info(f"Found {len(audio_files)} audio file(s)")

    # Validate filename format and parse tracks
    tracks = []
    sample_rates = set()

    for audio_path in audio_files:
        track = TrackInfo.from_filename(audio_path)
        if track is None:
            result.add_error(
                f"Invalid filename format: {audio_path.name}\n"
                f"  Expected: NN__Title__Mood__Genre__BPM.mp3 (or .wav)"
            )
            continue

        # Check audio integrity
        audio_info = get_audio_info(audio_path)
        if 'error' in audio_info:
            result.add_error(f"Audio integrity check failed for {audio_path.name}: {audio_info['error']}")
            continue

        if audio_info['duration'] <= 0:
            result.add_error(f"Invalid duration (<=0) for {audio_path.name}")
            continue

        track.duration = audio_info['duration']
        track.sample_rate = audio_info['sample_rate']
        track.sha256 = compute_sha256(audio_path)

        sample_rates.add(track.sample_rate)
        tracks.append(track)

        log_success(f"  {track.order:02d}. {track.title} ({track.duration:.1f}s, {track.sample_rate}Hz)")

    # Check sample rate consistency
    if len(sample_rates) > 1:
        result.add_warning(
            f"Inconsistent sample rates detected: {sorted(sample_rates)}\n"
            f"  This may cause issues during merging."
        )

    # Check required media files
    if not paths.loop_video.exists():
        result.add_error(f"Missing loop video: {paths.loop_video}")
    else:
        video_info = get_video_info(paths.loop_video)
        if 'error' in video_info:
            result.add_error(f"Loop video integrity check failed: {video_info['error']}")
        else:
            log_success(f"Loop video: {video_info['width']}x{video_info['height']}, {video_info['duration']:.1f}s")

    if not paths.thumbnail.exists():
        result.add_error(f"Missing thumbnail: {paths.thumbnail}")
    else:
        log_success(f"Thumbnail found: {paths.thumbnail.name}")

    # Sort tracks by order
    result.tracks = sorted(tracks, key=lambda t: t.order)

    # Check for duplicate order numbers
    orders = [t.order for t in result.tracks]
    if len(orders) != len(set(orders)):
        result.add_error("Duplicate track order numbers detected")

    return result


# =============================================================================
# FFMPEG FILTER GRAPH CONSTRUCTION
# =============================================================================

def build_sequential_acrossfade_filter(
    num_tracks: int,
    crossfade_sec: float = DEFAULT_CROSSFADE_SEC,
    curve: str = 'tri'
) -> tuple[str, str]:
    """
    Build a sequential acrossfade filter graph.

    For N tracks, creates:
    [0][1]acrossfade=d=0.8:c1=tri:c2=tri[a01];
    [a01][2]acrossfade=d=0.8:c1=tri:c2=tri[a02];
    ...
    [aN-2][N-1]acrossfade=d=0.8:c1=tri:c2=tri[aFINAL]

    Returns:
        tuple: (filter_complex string, final output label)
    """
    if num_tracks < 2:
        raise ValueError("Need at least 2 tracks to build crossfade filter")

    filters = []

    # First crossfade: [0][1]acrossfade[a01]
    filters.append(
        f"[0][1]acrossfade=d={crossfade_sec}:c1={curve}:c2={curve}[a01]"
    )

    # Subsequent crossfades: [a01][2] -> [a02], [a02][3] -> [a03], ...
    for i in range(2, num_tracks):
        prev_label = f"a{str(i-1).zfill(2)}"  # a01, a02, a03, ...
        curr_label = f"a{str(i).zfill(2)}"    # a02, a03, a04, ...
        filters.append(
            f"[{prev_label}][{i}]acrossfade=d={crossfade_sec}:c1={curve}:c2={curve}[{curr_label}]"
        )

    final_label = f"a{str(num_tracks-1).zfill(2)}"
    filter_complex = ";".join(filters)

    return filter_complex, final_label


def calculate_merged_duration(tracks: list[TrackInfo], crossfade_sec: float) -> float:
    """Calculate expected duration after crossfade merge."""
    if not tracks:
        return 0.0
    if len(tracks) == 1:
        return tracks[0].duration

    total = sum(t.duration for t in tracks)
    # Each crossfade removes crossfade_sec from total
    overlap_reduction = crossfade_sec * (len(tracks) - 1)
    return total - overlap_reduction


# =============================================================================
# FFMPEG OPERATIONS
# =============================================================================

def merge_tracks_with_crossfade(
    tracks: list[TrackInfo],
    output_path: Path,
    crossfade_sec: float = DEFAULT_CROSSFADE_SEC,
    sample_rate: int = 44100
) -> bool:
    """
    Merge multiple audio tracks using sequential acrossfade filter.

    Uses subprocess for maximum control over the FFmpeg command.
    """
    if len(tracks) < 2:
        if len(tracks) == 1:
            # Single track: just copy
            shutil.copy(tracks[0].path, output_path)
            return True
        return False

    # Build the filter complex
    filter_complex, final_label = build_sequential_acrossfade_filter(
        len(tracks), crossfade_sec
    )

    # Build FFmpeg command
    cmd = ['ffmpeg', '-y']

    # Add all input files
    for track in tracks:
        cmd.extend(['-i', str(track.path)])

    # Add filter complex
    cmd.extend([
        '-filter_complex', filter_complex,
        '-map', f'[{final_label}]',
        '-ar', str(sample_rate),
        '-ac', '2',
        str(output_path)
    ])

    log_info(f"Merging {len(tracks)} tracks with {crossfade_sec}s crossfade...")
    log_info(f"Filter graph: {filter_complex[:100]}..." if len(filter_complex) > 100 else f"Filter graph: {filter_complex}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        log_success(f"Merged audio saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"FFmpeg merge failed: {e.stderr}")
        return False


def trim_audio(input_path: Path, output_path: Path, duration_sec: float) -> bool:
    """Trim audio to specified duration."""
    try:
        (
            ffmpeg
            .input(str(input_path))
            .output(str(output_path), t=duration_sec, acodec='copy')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return True
    except ffmpeg.Error as e:
        log_error(f"Trim failed: {e.stderr.decode() if e.stderr else str(e)}")
        return False


def normalize_track(
    input_path: Path,
    output_path: Path,
    target_lufs: float = DEFAULT_LUFS,
    true_peak: float = DEFAULT_TRUE_PEAK
) -> bool:
    """
    Normalize a single track using ffmpeg-normalize.
    Uses python -m to ensure module is found regardless of PATH.
    """
    cmd = [
        sys.executable, '-m', 'ffmpeg_normalize',
        str(input_path),
        '-o', str(output_path),
        '-t', str(target_lufs),
        '-tp', str(true_peak),
        '-ar', '44100',
        '-f',  # Force overwrite
        '-pr'  # Progress bar
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Normalization failed for {input_path.name}: {e.stderr}")
        return False
    except FileNotFoundError:
        log_error("ffmpeg-normalize not found. Install with: pip install ffmpeg-normalize")
        return False


def render_video(
    audio_path: Path,
    loop_video_path: Path,
    thumbnail_path: Path,
    output_path: Path,
    use_shortest: bool = True
) -> bool:
    """
    Render final video with looped background and audio.

    Uses -stream_loop -1 for infinite video loop and -shortest to stop at audio end.
    """
    # Get audio duration for logging
    audio_info = get_audio_info(audio_path)
    audio_duration = audio_info.get('duration', 0)
    log_info(f"Rendering video with audio duration: {audio_duration:.1f}s")

    # Build FFmpeg command with proper loop handling
    cmd = [
        'ffmpeg', '-y',
        '-stream_loop', '-1',  # Loop video infinitely
        '-i', str(loop_video_path),
        '-i', str(audio_path),
        '-i', str(thumbnail_path),  # Thumbnail as attachment
        '-map', '0:v',
        '-map', '1:a',
        '-c:v', VIDEO_CODEC,
        '-preset', VIDEO_PRESET,
        '-crf', str(VIDEO_CRF),
        '-c:a', AUDIO_CODEC,
        '-b:a', AUDIO_BITRATE,
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
    ]

    if use_shortest:
        cmd.append('-shortest')

    cmd.append(str(output_path))

    try:
        log_info("Running FFmpeg render...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        log_success(f"Video rendered to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Video render failed: {e.stderr}")
        return False


def create_video_crossfade(
    loop_path: Path,
    output_path: Path,
    target_duration: float,
    fade_duration: float = 0.5
) -> bool:
    """
    Create crossfaded loop video using FFmpeg xfade filter.

    This function creates a seamless looping video by applying xfade
    transitions between repeated copies of the source video.

    Args:
        loop_path: Path to source loop video
        output_path: Path for output video
        target_duration: Target duration in seconds
        fade_duration: Crossfade duration in seconds (default: 0.5)

    Returns:
        True if successful, False otherwise
    """
    import math

    # Get loop video duration
    info = get_video_info(loop_path)
    loop_duration = info.get('duration', 0)

    if loop_duration <= 0:
        log_error("Cannot determine loop video duration")
        return False

    if loop_duration <= fade_duration:
        log_error(f"Loop duration ({loop_duration}s) must be greater than fade ({fade_duration}s)")
        return False

    # Calculate number of repeats needed
    effective_duration = loop_duration - fade_duration
    num_repeats = math.ceil(target_duration / effective_duration) + 1

    # Limit to prevent excessive memory usage
    if num_repeats > 100:
        log_warning(f"Large repeat count ({num_repeats}), capping at 100")
        num_repeats = 100

    log_info(f"Loop: {loop_duration:.1f}s, Target: {target_duration:.1f}s, Repeats: {num_repeats}")

    # Build FFmpeg command with xfade filter chain
    inputs = []
    for _ in range(num_repeats):
        inputs.extend(['-i', str(loop_path)])

    # Build xfade filter chain
    filter_parts = []

    # First xfade: [0:v][1:v] -> [v1]
    offset = loop_duration - fade_duration
    filter_parts.append(
        f"[0:v][1:v]xfade=transition=fade:duration={fade_duration}:offset={offset:.2f}[v1]"
    )

    # Subsequent xfades: [vN-1][N:v] -> [vN]
    for i in range(2, num_repeats):
        prev_label = f"v{i-1}"
        curr_label = f"v{i}"
        curr_offset = offset + (i - 1) * effective_duration
        filter_parts.append(
            f"[{prev_label}][{i}:v]xfade=transition=fade:duration={fade_duration}:offset={curr_offset:.2f}[{curr_label}]"
        )

    final_label = f"v{num_repeats - 1}"
    filter_complex = ";".join(filter_parts)

    cmd = [
        'ffmpeg', '-y',
        *inputs,
        '-filter_complex', filter_complex,
        '-map', f'[{final_label}]',
        '-c:v', VIDEO_CODEC,
        '-preset', 'fast',
        '-crf', str(VIDEO_CRF),
        '-pix_fmt', 'yuv420p',
        '-an',
        str(output_path)
    ]

    try:
        log_info("Creating video crossfade (this may take a while)...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        log_success(f"Video crossfade created: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Video crossfade failed: {e.stderr[-500:] if e.stderr else 'Unknown error'}")
        return False


# =============================================================================
# ARTIFACT GENERATION
# =============================================================================

def generate_provenance(
    tracks: list[TrackInfo],
    output_path: Path,
    params: dict
) -> bool:
    """Generate provenance.md with processing details."""
    timestamp = datetime.now().isoformat()

    content = [
        "# Provenance Report",
        "",
        f"Generated: {timestamp}",
        "",
        "## Processing Parameters",
        "",
        f"- Target LUFS: {params.get('lufs', DEFAULT_LUFS)}",
        f"- True Peak: {params.get('tp', DEFAULT_TRUE_PEAK)} dBTP",
        f"- Crossfade: {params.get('fade', DEFAULT_CROSSFADE_SEC)}s",
        "",
        "## Track Details",
        "",
        "| # | Filename | SHA-256 | Duration | Sample Rate |",
        "|---|----------|---------|----------|-------------|",
    ]

    for track in tracks:
        content.append(
            f"| {track.order:02d} | {track.path.name} | `{track.sha256[:16]}...` | "
            f"{track.duration:.1f}s | {track.sample_rate}Hz |"
        )

    content.extend([
        "",
        "## SHA-256 Full Hashes",
        "",
    ])

    for track in tracks:
        content.append(f"- `{track.path.name}`: `{track.sha256}`")

    try:
        output_path.write_text("\n".join(content), encoding='utf-8')
        log_success(f"Provenance saved to: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to write provenance: {e}")
        return False


# =============================================================================
# TITLE GENERATION (SSOT v1.5)
# =============================================================================

@dataclass
class TitleMeta:
    """Metadata for playlist title generation (SSOT v1.5)."""
    context_mode: Optional[str] = None  # Settling, Transition, Energizing, Focusing
    time_display: Optional[str] = None  # "AM 02:30" or "PM 10:00"
    time_state_phrase: Optional[str] = None  # 잠들지 못한 시간
    modifier_phrase: Optional[str] = None  # 천천히 흐르는
    genre: Optional[str] = None  # Slow R&B 보컬


def parse_title_meta(project_path: Path) -> TitleMeta:
    """
    Parse title metadata from concept.md.

    Expected format in concept.md:
    ```
    ## Title Meta
    - Context Mode: Settling
    - Time: AM 02:30
    - TIME_STATE_PHRASE: 잠들지 못한 시간
    - MODIFIER_PHRASE: 천천히 흐르는
    - GENRE: Slow R&B 보컬
    ```
    """
    meta = TitleMeta()
    concept_path = project_path / "concept.md"

    if not concept_path.exists():
        return meta

    content = concept_path.read_text(encoding='utf-8')

    # Parse key-value pairs
    patterns = {
        'context_mode': r'Context Mode[:\s]+(.+)',
        'time_display': r'Time[:\s]+([AP]M\s*\d{1,2}:\d{2})',
        'time_state_phrase': r'TIME_STATE_PHRASE[:\s]+(.+)',
        'modifier_phrase': r'MODIFIER_PHRASE[:\s]+(.+)',
        'genre': r'GENRE[:\s]+(.+)',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            setattr(meta, key, match.group(1).strip())

    return meta


def infer_context_mode(moods: set[str], detected_time: str) -> str:
    """Infer Context Mode from moods and time."""
    mood_lower = {m.lower() for m in moods}

    # Mood-based inference
    settling_moods = {'melancholic', 'sentimental', 'calm', 'hazy', 'ethereal'}
    energizing_moods = {'energetic', 'upbeat', 'powerful', 'driving'}
    focusing_moods = {'focused', 'steady', 'neutral'}

    if settling_moods & mood_lower:
        return 'Settling'
    elif energizing_moods & mood_lower:
        return 'Energizing'
    elif focusing_moods & mood_lower:
        return 'Focusing'

    # Time-based fallback
    time_defaults = {
        '새벽': 'Settling',
        '밤': 'Settling',
        '아침': 'Transition',
        '저녁': 'Transition',
        '오후': 'Focusing',
    }
    return time_defaults.get(detected_time, 'Settling')


def infer_time_display(detected_time: str) -> str:
    """Infer time display from detected time keyword."""
    time_mapping = {
        '새벽': 'AM 02:30',
        '밤': 'PM 11:00',
        '아침': 'AM 07:00',
        '저녁': 'PM 07:00',
        '오후': 'PM 03:00',
    }
    return time_mapping.get(detected_time, 'PM 10:00')


def infer_time_state_phrase(context_mode: str, phrase_type: str = 'A') -> str:
    """Infer TIME_STATE_PHRASE based on Context Mode."""
    phrases = {
        'Settling': {
            'A': '잠들지 못한 시간',
            'B': '소리가 낮아진 시간',
        },
        'Transition': {
            'A': '하루를 풀어내는 시간',
            'B': '빛이 바뀌는 시간',
        },
        'Energizing': {
            'A': '다시 움직이기 전의 시간',
            'B': '주변이 바빠지기 전의 시간',
        },
        'Focusing': {
            'A': '하루가 멈춘 시간',
            'B': '움직임이 느려진 시간',
        },
    }
    return phrases.get(context_mode, phrases['Settling']).get(phrase_type, phrases['Settling']['A'])


def infer_modifier_phrase(context_mode: str) -> str:
    """Infer MODIFIER_PHRASE based on Context Mode."""
    modifiers = {
        'Settling': '천천히 흐르는',
        'Transition': '부드럽게 이어지는',
        'Energizing': '경쾌하게 흐르는',
        'Focusing': '낮게 이어지는',
    }
    return modifiers.get(context_mode, '조용히 흐르는')


def infer_genre_label(genres: set[str]) -> str:
    """Infer genre label from track genres."""
    genre_lower = {g.lower().replace('-', ' ') for g in genres}

    # Priority mapping
    if any('rnb' in g or 'r&b' in g for g in genre_lower):
        if any('ballad' in g for g in genre_lower):
            return 'Slow R&B 보컬'
        return 'R&B 보컬'
    elif any('rock' in g for g in genre_lower):
        if any('indie' in g for g in genre_lower):
            return 'Indie Rock'
        return '미디엄 템포 Rock'
    elif any('jazz' in g for g in genre_lower):
        return 'Quiet Jazz Vocals'
    elif any('pop' in g for g in genre_lower):
        return 'Vocal Pop'

    # Default
    return 'R&B 보컬'


def generate_title(
    meta: TitleMeta,
    genres: set[str],
    detected_time: str,
    moods: set[str]
) -> str:
    """
    Generate playlist title following SSOT v1.5 rules.

    Format: [Playlist] [AM/PM HH:MM] soomshuim | {TIME_STATE_PHRASE}, {MODIFIER_PHRASE} {GENRE}
    """
    # Use meta values or infer
    context_mode = meta.context_mode or infer_context_mode(moods, detected_time)
    time_display = meta.time_display or infer_time_display(detected_time)
    time_state = meta.time_state_phrase or infer_time_state_phrase(context_mode)
    modifier = meta.modifier_phrase or infer_modifier_phrase(context_mode)
    genre = meta.genre or infer_genre_label(genres)

    # Build title
    title = f"[Playlist] [{time_display}] soomshuim | {time_state}, {modifier} {genre}"

    return title


def generate_intro_and_comment(series_name: str, moods: set[str]) -> tuple[str, str]:
    """
    Generate custom intro paragraph and pinned comment based on series concept.

    Returns: (intro_text, pinned_comment)
    """
    # Time/concept detection from series name
    time_keywords = {
        '새벽': ('dawn', '새벽'),
        '밤': ('night', '밤'),
        '저녁': ('evening', '저녁'),
        '아침': ('morning', '아침'),
        '오후': ('afternoon', '오후'),
        '잠': ('sleep', '새벽'),
    }

    detected_time = None
    for keyword, (eng, kor) in time_keywords.items():
        if keyword in series_name:
            detected_time = kor
            break

    # Default to generic if no time detected
    if not detected_time:
        detected_time = '밤'

    # Mood-based description hints
    mood_lower = {m.lower() for m in moods}
    is_melancholic = any(m in mood_lower for m in ['melancholic', 'sentimental', 'sad'])
    is_calm = any(m in mood_lower for m in ['chill', 'calm', 'ethereal', 'hazy'])
    is_hopeful = any(m in mood_lower for m in ['hopeful', 'warm', 'bright'])

    # Generate intro based on time and mood
    if detected_time == '새벽':
        if is_melancholic or is_calm:
            intro = """잠이 오지 않는 밤에 듣기 좋은 노래들을 모았습니다.
조용히 흘려듣기에도, 가만히 붙잡고 듣기에도 괜찮은 음악들입니다.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘은 조금 더 천천히 닿기를 바라며.

🎧 이어폰 착용을 추천합니다."""
            comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘도 수고 많았어요.
여기 모인 모든 분들, 푹 주무세요. 🌙"""
        else:
            intro = """새벽의 고요함 속에서 듣기 좋은 노래들입니다.
하루를 마무리하며, 혹은 새로운 하루를 준비하며.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘은 조금 더 가깝게 닿기를 바라며.

🎧 이어폰 착용을 추천합니다."""
            comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루도 고생 많으셨어요.
편안한 밤 되세요. 🌙"""
    elif detected_time == '밤':
        intro = """밤에 듣기 좋은 노래들을 모았습니다.
조용히 흘려듣기에도, 가만히 집중해서 듣기에도 좋은 음악들입니다.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘 밤은 조금 다르게 들리기를 바라며.

🎧 이어폰 착용을 추천합니다."""
        comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루 어떠셨나요?
편안한 밤 보내세요. 🌃"""
    elif detected_time == '저녁':
        intro = """하루를 마무리하며 듣기 좋은 노래들입니다.
분주했던 시간을 내려놓고, 잠시 쉬어가는 음악들.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘 저녁은 조금 더 따뜻하게 닿기를 바라며.

🎧 이어폰 착용을 추천합니다."""
        comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루도 수고하셨어요.
따뜻한 저녁 되세요. 🌅"""
    elif detected_time == '아침':
        intro = """아침에 듣기 좋은 노래들을 모았습니다.
새로운 하루를 여는, 조용하지만 힘이 되는 음악들.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘 아침은 조금 더 선명하게 닿기를 바라며.

🎧 이어폰 착용을 추천합니다."""
        comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

좋은 아침이에요.
오늘 하루도 잘 보내세요. ☀️"""
    else:  # 오후 or default
        intro = """편안하게 듣기 좋은 노래들을 모았습니다.
흘려듣기에도, 집중해서 듣기에도 좋은 음악들.

이 플레이리스트의 노래들은 모두 우리말 가사로 만들어졌어요.
익숙한 말이, 오늘은 조금 다르게 닿기를 바라며.

🎧 이어폰 착용을 추천합니다."""
        comment = """이 채널의 노래들은 모두 우리말 가사로 만들어졌습니다.
익숙한 말들이 더 천천히, 더 깊게 닿기를 바랍니다.

오늘 하루 어떠세요?
좋은 시간 보내세요. 🎵"""

    return intro, comment


def generate_description(
    tracks: list[TrackInfo],
    output_path: Path,
    crossfade_sec: float,
    series_name: str = "",
    project_path: Optional[Path] = None
) -> bool:
    """Generate draft_description.txt with title draft, intro, timestamps, hashtags, and pinned comment."""
    lines = []
    current_time = 0.0

    # Collect all unique moods/genres for context
    all_moods = set()
    all_genres = set()

    for track in tracks:
        all_moods.add(track.mood)
        all_genres.add(track.genre)

    # Detect time from series name
    time_keywords = {
        '새벽': '새벽', '밤': '밤', '저녁': '저녁',
        '아침': '아침', '오후': '오후', '잠': '새벽',
    }
    detected_time = '밤'  # default
    for keyword, time_val in time_keywords.items():
        if keyword in series_name:
            detected_time = time_val
            break

    # === TITLE DRAFT (SSOT v1.5) ===
    if project_path:
        title_meta = parse_title_meta(project_path)
    else:
        title_meta = TitleMeta()

    generated_title = generate_title(title_meta, all_genres, detected_time, all_moods)

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📋 제목 초안 (SSOT v1.5)")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(generated_title)
    lines.append("")
    lines.append("▸ 위 제목은 자동 생성된 초안입니다.")
    lines.append("▸ concept.md에 Title Meta를 추가하면 커스터마이즈 가능합니다.")
    lines.append("")
    lines.append("")

    # Generate custom intro and pinned comment
    intro_text, pinned_comment = generate_intro_and_comment(series_name, all_moods)

    # Add intro
    lines.append(intro_text)
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━")

    # Generate timestamps (single pass, no repeat labels)
    for track in tracks:
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        lines.append(f"{timestamp} {track.order:02d}. {track.title}")

        # Next track starts after this duration minus crossfade overlap
        if track != tracks[-1]:
            current_time += track.duration - crossfade_sec
        else:
            current_time += track.duration

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    # Hashtags
    common_hashtags = [
        "#감성플레이리스트",
        "#플레이리스트",
        "#한국어플레이리스트",
        "#가사좋은노래",
    ]

    track_hashtags = []
    for mood in sorted(all_moods):
        track_hashtags.append(f"#{mood.replace(' ', '')}")
    for genre in sorted(all_genres):
        tag = f"#{genre.replace(' ', '').replace('-', '')}플레이리스트"
        if tag not in track_hashtags:
            track_hashtags.append(tag)

    lines.append(" ".join(common_hashtags + track_hashtags))
    lines.append("All tracks feature Korean lyrics.")

    # Add pinned comment section
    lines.extend([
        "",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📌 고정 댓글용",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "",
        pinned_comment,
    ])

    try:
        output_path.write_text("\n".join(lines), encoding='utf-8')
        log_success(f"Description saved to: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to write description: {e}")
        return False


def generate_upload_csv(
    paths: ProjectPaths,
    tracks: list[TrackInfo],
    output_path: Path
) -> bool:
    """Generate upload.csv for batch uploading."""
    # Generate title from first few tracks or folder name
    series_name = paths.base.parent.name if paths.base.parent != paths.base else "Playlist"
    date_str = paths.base.name
    title = f"{series_name} - {date_str}"

    # Collect tags
    tags = set()
    for track in tracks:
        tags.add(track.mood)
        tags.add(track.genre)

    row = {
        'video_path': str(paths.final_mp4),
        'title': title,
        'description': str(paths.draft_description),
        'tags': ','.join(sorted(tags)),
        'thumbnail_path': str(paths.thumbnail),
        'visibility': 'private'  # Default to private for safety
    }

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            writer.writerow(row)
        log_success(f"Upload CSV saved to: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to write upload CSV: {e}")
        return False


def generate_report(
    tracks: list[TrackInfo],
    output_path: Path,
    final_duration: float,
    params: dict
) -> bool:
    """Generate report.json with technical statistics."""
    report = {
        'generated_at': datetime.now().isoformat(),
        'processing_params': params,
        'summary': {
            'total_tracks': len(tracks),
            'total_original_duration': sum(t.duration for t in tracks),
            'final_duration': final_duration,
            'crossfade_reduction': sum(t.duration for t in tracks) - final_duration,
        },
        'tracks': [
            {
                'order': t.order,
                'title': t.title,
                'mood': t.mood,
                'genre': t.genre,
                'bpm': t.bpm,
                'duration': t.duration,
                'sample_rate': t.sample_rate,
                'sha256': t.sha256,
                'filename': t.path.name,
            }
            for t in tracks
        ]
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        log_success(f"Report saved to: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to write report: {e}")
        return False


# =============================================================================
# UTILITY FUNCTIONS - TIME PARSING
# =============================================================================

def parse_time_string(time_str: str) -> float:
    """
    Parse time string in MM:SS or HH:MM:SS format to seconds.

    Examples:
        "00:45" -> 45.0
        "01:30" -> 90.0
        "1:05:30" -> 3930.0
    """
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        raise ValueError(f"Invalid time format: {time_str}. Expected MM:SS or HH:MM:SS")


# =============================================================================
# CLI COMMANDS
# =============================================================================

@click.group()
@click.version_option(version='1.0.0', prog_name='vibem')
def cli():
    """
    vibem - YouTube Music Playlist Generation CLI

    Automate the creation of YouTube music playlist videos with
    professional audio processing and crossfade transitions.
    """
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
def validate(path: Path):
    """
    Validate project structure and files.

    Performs health checks before processing:
    - Verifies tracks exist with valid filenames
    - Checks audio integrity via ffprobe
    - Validates required media files (loop.mp4, thumb.jpg)
    - Reports sample rate consistency
    """
    click.echo(click.style("\n=== VIBEM VALIDATION ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)
    result = validate_project(paths)

    # Print summary
    click.echo("")

    if result.warnings:
        click.echo(click.style("Warnings:", fg='yellow', bold=True))
        for warning in result.warnings:
            log_warning(warning)
        click.echo("")

    if result.errors:
        click.echo(click.style("Errors:", fg='red', bold=True))
        for error in result.errors:
            log_error(error)
        click.echo("")
        click.echo(click.style("VALIDATION FAILED", fg='red', bold=True))
        sys.exit(1)

    # Success summary
    total_duration = sum(t.duration for t in result.tracks)
    click.echo(click.style("Summary:", fg='green', bold=True))
    click.echo(f"  Tracks: {len(result.tracks)}")
    click.echo(f"  Total Duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")
    click.echo("")
    click.echo(click.style("VALIDATION PASSED", fg='green', bold=True))


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--sec', default=DEFAULT_PREVIEW_SEC, help='Preview duration in seconds')
@click.option('--fade', default=DEFAULT_CROSSFADE_SEC, help='Crossfade duration in seconds')
def preview(path: Path, sec: int, fade: float):
    """
    Generate a quick preview video.

    Creates a fast preview by:
    - Taking first N seconds from EACH track (sec / num_tracks)
    - Merging trimmed tracks with crossfade (no normalization)
    - Rendering with loop video

    This ensures all tracks are represented in the preview.

    Output: output/preview.mp4
    """
    click.echo(click.style("\n=== VIBEM PREVIEW ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)

    # Validate first
    log_info("Running validation...")
    result = validate_project(paths)

    if not result.is_valid:
        for error in result.errors:
            log_error(error)
        click.echo(click.style("\nVALIDATION FAILED - Cannot generate preview", fg='red', bold=True))
        sys.exit(1)

    if not result.tracks:
        log_error("No valid tracks found")
        sys.exit(1)

    # Ensure output directories
    paths.ensure_work_dirs()

    num_tracks = len(result.tracks)

    if num_tracks == 1:
        # Single track: trim and use directly
        log_info("Single track detected...")
        trimmed_path = paths.work_dir / 'preview_trimmed.wav'
        trim_duration = min(sec, result.tracks[0].duration)

        if not trim_audio(result.tracks[0].path, trimmed_path, trim_duration):
            log_error("Failed to trim audio")
            sys.exit(1)
    else:
        # Multiple tracks: trim each track first, then merge
        # Calculate duration per track (accounting for crossfade overlap)
        # Crossfade overlaps: (num_tracks - 1) * fade seconds are shared
        # So we need: sec + (num_tracks - 1) * fade total track time
        total_track_time = sec + (num_tracks - 1) * fade
        sec_per_track = total_track_time / num_tracks

        log_info(f"Trimming each track to {sec_per_track:.1f}s for {sec}s preview...")

        # Trim each track
        trimmed_tracks = []
        for i, track in enumerate(result.tracks):
            trimmed_path_i = paths.work_dir / f'preview_track_{i:02d}.wav'
            trim_duration = min(sec_per_track, track.duration)

            log_info(f"  Trimming {track.title} to {trim_duration:.1f}s...")
            if not trim_audio(track.path, trimmed_path_i, trim_duration):
                log_error(f"Failed to trim track {track.title}")
                sys.exit(1)

            # Create a temporary TrackInfo with the trimmed path
            trimmed_track = TrackInfo(
                path=trimmed_path_i,
                order=track.order,
                title=track.title,
                mood=track.mood,
                genre=track.genre,
                bpm=track.bpm,
                duration=trim_duration,
                sample_rate=track.sample_rate
            )
            trimmed_tracks.append(trimmed_track)

        # Merge trimmed tracks with crossfade
        merged_path = paths.work_dir / 'preview_merged.wav'
        log_info(f"Merging {num_tracks} trimmed tracks with {fade}s crossfade...")

        if not merge_tracks_with_crossfade(trimmed_tracks, merged_path, fade):
            log_error("Failed to merge tracks")
            sys.exit(1)

        trimmed_path = merged_path

    # Render video
    # Get actual duration of the audio
    audio_info = get_audio_info(trimmed_path)
    audio_duration = audio_info.get('duration', 0)
    log_info(f"Rendering video with audio duration: {audio_duration:.1f}s")

    if not render_video(
        trimmed_path,
        paths.loop_video,
        paths.thumbnail,
        paths.preview_mp4,
        use_shortest=True
    ):
        log_error("Failed to render video")
        sys.exit(1)

    # Summary
    click.echo("")
    click.echo(click.style("PREVIEW COMPLETE", fg='green', bold=True))
    click.echo(f"Output: {paths.preview_mp4}")
    if num_tracks > 1:
        click.echo(f"Duration: {audio_duration:.1f}s ({num_tracks} tracks × ~{sec_per_track:.1f}s each)")


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--lufs', default=DEFAULT_LUFS, help='Target loudness in LUFS')
@click.option('--tp', default=DEFAULT_TRUE_PEAK, help='True peak in dBTP')
@click.option('--fade', default=DEFAULT_CROSSFADE_SEC, help='Crossfade duration in seconds')
@click.option('--skip-normalize', is_flag=True, help='Skip normalization step')
@click.option('--repeat', default=2, help='Number of times to repeat the playlist (default: 2)')
@click.option('--use-xfade', is_flag=True, help='Use loop_xfade.mp4 for video (recommended)')
@click.option('--force', is_flag=True, help='Skip video crossfade confirmation')
def pack(path: Path, lufs: float, tp: float, fade: float, skip_normalize: bool, repeat: int, use_xfade: bool, force: bool):
    """
    Create final deliverables for YouTube.

    Full production workflow:
    0. Pre-flight check (video crossfade)
    1. Validate project structure
    2. Normalize each track (ffmpeg-normalize)
    3. Merge with sequential crossfade (repeated N times, default 2x)
    4. Render final video
    5. Generate artifacts (provenance, description, upload CSV, report)

    Output: output/final.mp4 + artifacts

    RECOMMENDED: Use --use-xfade for seamless video loops.
    First run 'vfade --test' to verify, then 'vfade' to create loop_xfade.mp4.
    """
    click.echo(click.style("\n=== VIBEM PACK ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)
    params = {'lufs': lufs, 'tp': tp, 'fade': fade, 'repeat': repeat, 'use_xfade': use_xfade}

    # Step 0: Pre-flight check for video crossfade
    log_info("Step 0/6: Pre-flight check...")

    if use_xfade:
        if not paths.loop_xfade.exists():
            log_error(f"--use-xfade specified but {paths.loop_xfade.name} not found!")
            log_warning("Run 'python3 vibem.py vfade <path>' first to create it.")
            sys.exit(1)
        log_success(f"Using crossfaded video: {paths.loop_xfade.name}")
    else:
        if paths.loop_xfade.exists():
            log_info(f"Found {paths.loop_xfade.name} - consider using --use-xfade")
        else:
            log_warning("No loop_xfade.mp4 found - video will have visible cuts at loop boundaries!")
            log_warning("To fix: python3 vibem.py vfade <path> --test  # then verify")
            log_warning("        python3 vibem.py vfade <path>         # create full version")
            log_warning("        python3 vibem.py pack <path> --use-xfade")

            if not force:
                if not click.confirm("Continue with loop.mp4 (visible cuts)?", default=False):
                    click.echo("Aborted. Run 'vfade' first to create seamless loop video.")
                    sys.exit(0)

    # Step 1: Validate
    log_info("Step 1/6: Validation...")
    result = validate_project(paths)

    if not result.is_valid:
        for error in result.errors:
            log_error(error)
        click.echo(click.style("\nVALIDATION FAILED - Cannot proceed", fg='red', bold=True))
        sys.exit(1)

    if not result.tracks:
        log_error("No valid tracks found")
        sys.exit(1)

    for warning in result.warnings:
        log_warning(warning)

    log_success(f"Validation passed: {len(result.tracks)} tracks")

    # Ensure directories
    paths.ensure_work_dirs()

    # Step 2: Normalize
    log_info(f"Step 2/6: Normalizing tracks (Target: {lufs} LUFS, TP: {tp} dBTP)...")

    normalized_tracks = []

    if skip_normalize:
        log_warning("Skipping normalization (--skip-normalize)")
        normalized_tracks = result.tracks
    else:
        for i, track in enumerate(result.tracks, 1):
            norm_path = paths.norm_tracks_dir / f"norm_{track.path.stem}.wav"
            log_info(f"  [{i}/{len(result.tracks)}] Normalizing {track.path.name}...")

            if not normalize_track(track.path, norm_path, lufs, tp):
                log_error(f"Failed to normalize {track.path.name}")
                sys.exit(1)

            # Create new track info with normalized path
            norm_track = TrackInfo(
                path=norm_path,
                order=track.order,
                title=track.title,
                mood=track.mood,
                genre=track.genre,
                bpm=track.bpm,
                duration=track.duration,
                sample_rate=track.sample_rate,
                sha256=track.sha256,  # Keep original hash for provenance
            )
            normalized_tracks.append(norm_track)

        log_success("Normalization complete")

    # Step 3: Merge with crossfade (with repeat)
    log_info(f"Step 3/6: Merging tracks with {fade}s crossfade (x{repeat} repeat)...")

    # Create repeated track list for merging
    tracks_to_merge = normalized_tracks * repeat
    log_info(f"  Total tracks to merge: {len(tracks_to_merge)} ({len(normalized_tracks)} tracks x {repeat})")

    if len(tracks_to_merge) == 1:
        log_info("Single track detected, converting to WAV...")
        (
            ffmpeg
            .input(str(tracks_to_merge[0].path))
            .output(str(paths.merged_wav), ar=44100, ac=2)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    else:
        if not merge_tracks_with_crossfade(tracks_to_merge, paths.merged_wav, fade):
            log_error("Failed to merge tracks")
            sys.exit(1)

    log_success("Merge complete")

    # Step 4: Render video
    log_info("Step 4/6: Rendering final video...")

    # Select video source based on --use-xfade flag
    video_source = paths.loop_xfade if use_xfade else paths.loop_video
    log_info(f"  Video source: {video_source.name}")

    if not render_video(
        paths.merged_wav,
        video_source,
        paths.thumbnail,
        paths.final_mp4,
        use_shortest=True
    ):
        log_error("Failed to render video")
        sys.exit(1)

    log_success("Video render complete")

    # Step 5: Generate artifacts
    log_info("Step 5/6: Generating artifacts...")

    # Get final duration
    final_info = get_audio_info(paths.merged_wav)
    final_duration = final_info.get('duration', 0)

    # Use original tracks for provenance (contains original hashes)
    generate_provenance(result.tracks, paths.provenance_md, params)

    # Get series name for description context
    series_name = paths.base.parent.name if paths.base.parent != paths.base else ""
    generate_description(result.tracks, paths.draft_description, fade, series_name, paths.base)

    generate_upload_csv(paths, result.tracks, paths.upload_csv)
    generate_report(result.tracks, paths.report_json, final_duration, params)

    # Final summary
    click.echo("")
    click.echo(click.style("=" * 50, fg='green'))
    click.echo(click.style("PACK COMPLETE", fg='green', bold=True))
    click.echo(click.style("=" * 50, fg='green'))
    click.echo("")
    click.echo("Deliverables:")
    click.echo(f"  Video:       {paths.final_mp4}")
    click.echo(f"  Provenance:  {paths.provenance_md}")
    click.echo(f"  Description: {paths.draft_description}")
    click.echo(f"  Upload CSV:  {paths.upload_csv}")
    click.echo(f"  Report:      {paths.report_json}")
    click.echo("")
    click.echo(f"Total tracks:   {len(result.tracks)} (x{repeat} = {len(result.tracks) * repeat} plays)")
    click.echo(f"Final duration: {final_duration:.1f}s ({final_duration/60:.1f} min)")
    click.echo(f"Repeat:         {repeat}x")


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option('--fade', default=0.5, help='Crossfade duration in seconds (default: 0.5)')
@click.option('--duration', default=0, help='Target duration in seconds (default: auto from audio)')
@click.option('--test', is_flag=True, help='Generate 30-second test video only')
def vfade(path: Path, fade: float, duration: float, test: bool):
    """
    Create crossfaded loop video for seamless playback.

    This command applies FFmpeg xfade transitions to loop.mp4 to eliminate
    visible cuts when the video repeats.

    Workflow:
    1. Run with --test to generate a 30-second test video
    2. Verify the transitions are smooth
    3. Run without --test to generate the full video

    Output: input/loop_xfade.mp4 (or loop_xfade_test.mp4 for test mode)
    """
    click.echo(click.style("\n=== VIBEM VFADE ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)

    # Check loop.mp4 exists
    if not paths.loop_video.exists():
        log_error(f"Missing loop video: {paths.loop_video}")
        sys.exit(1)

    # Get loop video info
    loop_info = get_video_info(paths.loop_video)
    loop_duration = loop_info.get('duration', 0)

    if loop_duration <= 0:
        log_error("Cannot determine loop video duration")
        sys.exit(1)

    log_info(f"Source: {paths.loop_video.name} ({loop_duration:.1f}s)")

    # Determine target duration
    if test:
        target_duration = 30.0
        output_path = paths.loop_xfade_test
        log_info("Test mode: generating 30-second preview")
    else:
        if duration > 0:
            target_duration = duration
        else:
            # Auto-detect from merged audio if exists
            if paths.merged_wav.exists():
                audio_info = get_audio_info(paths.merged_wav)
                target_duration = audio_info.get('duration', 90.0)
                log_info(f"Auto-detected duration from merged.wav: {target_duration:.1f}s")
            else:
                # Default to 90 seconds for initial creation
                target_duration = 90.0
                log_warning("No merged.wav found, using default 90s duration")

        output_path = paths.loop_xfade

    log_info(f"Target duration: {target_duration:.1f}s")
    log_info(f"Crossfade: {fade}s")

    # Create video crossfade
    if not create_video_crossfade(paths.loop_video, output_path, target_duration, fade):
        log_error("Failed to create video crossfade")
        sys.exit(1)

    # Get output info
    output_info = get_video_info(output_path)
    output_duration = output_info.get('duration', 0)

    click.echo("")
    click.echo(click.style("=" * 50, fg='green'))
    click.echo(click.style("VFADE COMPLETE", fg='green', bold=True))
    click.echo(click.style("=" * 50, fg='green'))
    click.echo("")
    click.echo(f"Output:   {output_path}")
    click.echo(f"Duration: {output_duration:.1f}s ({output_duration/60:.1f} min)")
    click.echo(f"Fade:     {fade}s")

    if test:
        click.echo("")
        click.echo(click.style("Next steps:", fg='yellow'))
        click.echo(f"  1. Open and verify: open {output_path}")
        click.echo(f"  2. If smooth, run: python3 vibem.py vfade {path}")
    else:
        click.echo("")
        click.echo(click.style("Next steps:", fg='yellow'))
        click.echo(f"  Run: python3 vibem.py pack {path} --use-xfade")


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
def init(path: Path):
    """
    Initialize project directory structure.

    Creates the required folder structure:
    - input/tracks/
    - input/ (for loop.mp4 and thumb.jpg)
    - work/
    - output/
    """
    click.echo(click.style("\n=== VIBEM INIT ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)

    # Create directories
    ensure_dir(paths.input_dir)
    ensure_dir(paths.tracks_dir)
    ensure_dir(paths.work_dir)
    ensure_dir(paths.output_dir)

    log_success(f"Created: {paths.input_dir}")
    log_success(f"Created: {paths.tracks_dir}")
    log_success(f"Created: {paths.work_dir}")
    log_success(f"Created: {paths.output_dir}")

    click.echo("")
    click.echo("Next steps:")
    click.echo(f"  1. Add MP3 files to: {paths.tracks_dir}")
    click.echo(f"     Format: NN__Title__Mood__Genre__BPM.mp3")
    click.echo(f"  2. Add loop.mp4 to: {paths.input_dir}")
    click.echo(f"  3. Add thumb.jpg to: {paths.input_dir}")
    click.echo(f"  4. Run: vibem validate {path}")


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, path_type=Path))
def clean(path: Path):
    """
    Clean work and output directories.

    Removes all generated files while preserving input files.
    """
    click.echo(click.style("\n=== VIBEM CLEAN ===\n", fg='cyan', bold=True))

    paths = ProjectPaths(path)

    if paths.work_dir.exists():
        shutil.rmtree(paths.work_dir)
        log_success(f"Removed: {paths.work_dir}")

    if paths.output_dir.exists():
        shutil.rmtree(paths.output_dir)
        log_success(f"Removed: {paths.output_dir}")

    click.echo("")
    click.echo(click.style("CLEAN COMPLETE", fg='green', bold=True))


@cli.command()
@click.argument('track_path', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--start', required=True, help='Start time in MM:SS format (e.g., "00:45")')
@click.option('--duration', default=30, help='Duration in seconds (default: 30)')
@click.option('--title', default=None, help='Center title text (hook phrase, appears briefly)')
@click.option('--title-duration', default=4.0, help='Title display duration in seconds (default: 4)')
@click.option('--lyric', default=None, help='Bottom lyric text (atmospheric, stays throughout)')
@click.option('--lyric-delay', default=1.0, help='Lyric fade-in delay in seconds (default: 1)')
@click.option('--srt', default=None, type=click.Path(exists=True), help='SRT subtitle file for dynamic lyrics')
@click.option('--title-font', default=None, type=click.Path(exists=True), help='Title font (default: Pretendard Black)')
@click.option('--lyric-font', default=None, type=click.Path(exists=True), help='Lyric font (default: Pretendard Medium)')
def shorts(
    track_path: Path,
    start: str,
    duration: int,
    title: Optional[str],
    title_duration: float,
    lyric: Optional[str],
    lyric_delay: float,
    srt: Optional[Path],
    title_font: Optional[Path],
    lyric_font: Optional[Path],
):
    """
    Create a YouTube Shorts video from a track segment.

    Takes a specific MP3 file and creates a 9:16 vertical video
    suitable for YouTube Shorts.

    \b
    Text Options:
    - --title: Center hook phrase (0-2s display, 2-4s fade out)
    - --lyric: Bottom static text (fade in, stays until end)
    - --srt: Dynamic lyrics from SRT file (timed subtitles)

    \b
    Input:
    - TRACK_PATH: Path to the MP3 file
    - shorts.mp4 (8-10s base video) is taken from the parent input/ directory
    - The base video is looped to match audio duration

    \b
    Output: output/shorts/short_[TrackName].mp4

    \b
    Examples:
        # Basic (no text)
        python vibem.py shorts tracks/02__윤곽__...mp3 --start 00:45 --duration 30

        # With title + static lyric
        python vibem.py shorts tracks/02__윤곽__...mp3 --start 00:45 --duration 30 \\
            --title "잠들지 못한 새벽" --lyric "여명처럼 스며들어"

        # With title + dynamic lyrics (SRT)
        python vibem.py shorts tracks/02__윤곽__...mp3 --start 00:45 --duration 30 \\
            --title "잠들지 못한 새벽" --srt lyrics.srt
    """
    click.echo(click.style("\n=== VIBEM SHORTS ===\n", fg='cyan', bold=True))

    # Resolve paths
    # Track path structure: .../input/tracks/NN__Title__...mp3
    # shorts.mp4 should be in: .../input/shorts.mp4 (8-10s base video, will be looped)
    tracks_dir = track_path.parent
    input_dir = tracks_dir.parent
    base_dir = input_dir.parent
    shorts_video = input_dir / 'shorts.mp4'
    shorts_output_dir = base_dir / 'output' / 'shorts'

    # Validate track filename format
    track_info = TrackInfo.from_filename(track_path)
    if track_info is None:
        log_error(f"Invalid track filename format: {track_path.name}")
        log_error("Expected format: NN__Title__Mood__Genre__BPM.mp3")
        sys.exit(1)

    log_info(f"Track: {track_info.order:02d}. {track_info.title}")

    # Validate shorts base video exists
    if not shorts_video.exists():
        log_error(f"Shorts base video not found: {shorts_video}")
        log_error(f"Expected shorts.mp4 (8-10s) in: {input_dir}")
        sys.exit(1)

    log_success(f"Shorts base video found: {shorts_video}")

    # Parse start time
    try:
        start_sec = parse_time_string(start)
    except ValueError as e:
        log_error(str(e))
        sys.exit(1)

    log_info(f"Start time: {start} ({start_sec:.1f}s)")
    log_info(f"Duration: {duration}s")

    # Get audio info to validate segment
    audio_info = get_audio_info(track_path)
    if 'error' in audio_info:
        log_error(f"Failed to read audio: {audio_info['error']}")
        sys.exit(1)

    track_duration = audio_info['duration']
    if start_sec + duration > track_duration:
        log_warning(f"Requested segment exceeds track duration ({track_duration:.1f}s)")
        log_warning(f"Will use remaining audio from {start}s")

    # Ensure output directory
    ensure_dir(shorts_output_dir)

    # Output filename
    output_filename = f"short_{track_info.title}.mp4"
    output_path = shorts_output_dir / output_filename

    log_info(f"Output: {output_path}")

    # Build video filter
    # Base filter: 9:16 center crop
    crop_filter = "crop=ih*9/16:ih:(iw-ih*9/16)/2:0"

    # Determine text overlay mode
    # Priority: SRT (dynamic) > lyric (static)
    needs_drawtext = False
    needs_subtitles = False
    filters = [crop_filter]

    # SRT dynamic lyrics (takes priority over static lyric)
    if srt:
        srt_path = Path(srt).resolve()
        # Simple subtitles filter without force_style (force_style causes filter chain issues)
        # TODO: Fix force_style comma escaping to enable custom font/position
        srt_filter = f"subtitles='{srt_path}'"
        filters.append(srt_filter)
        needs_subtitles = True
        log_info(f"SRT: {srt_path.name} (dynamic lyrics)")

    # Title overlay (drawtext)
    if title:
        title_filter = build_text_overlay_filter(
            title=title,
            title_duration=title_duration,
            lyric=None,  # Don't add static lyric if SRT is provided
            lyric_delay=lyric_delay,
            title_font_path=str(title_font) if title_font else None,
            lyric_font_path=None,
        )
        if title_filter:
            filters.append(title_filter)
            needs_drawtext = True
            log_info(f"Title: {title}")

    # Static lyric (only if no SRT)
    if lyric and not srt:
        lyric_filter = build_text_overlay_filter(
            title=None,
            title_duration=title_duration,
            lyric=lyric,
            lyric_delay=lyric_delay,
            title_font_path=None,
            lyric_font_path=str(lyric_font) if lyric_font else None,
        )
        if lyric_filter:
            filters.append(lyric_filter)
            needs_drawtext = True
            log_info(f"Lyric: {lyric}")

    # Combine all filters
    video_filter = ",".join(filters)

    # Use ffmpeg-full when drawtext or subtitles is needed
    needs_advanced_ffmpeg = needs_drawtext or needs_subtitles
    ffmpeg_bin = get_ffmpeg_binary(needs_drawtext=needs_advanced_ffmpeg)
    if needs_advanced_ffmpeg and ffmpeg_bin != FFMPEG_DEFAULT:
        log_info(f"Using ffmpeg-full for text overlay")

    cmd = [
        ffmpeg_bin, '-y',
        # Video input: loop shorts.mp4 infinitely to match audio duration
        '-stream_loop', '-1',
        '-i', str(shorts_video),
        # Audio input: seek to start and limit duration
        '-ss', str(start_sec),
        '-t', str(duration),
        '-i', str(track_path),
        # Filter: center crop video to 9:16 + text overlay
        '-vf', video_filter,
        # Map streams
        '-map', '0:v',
        '-map', '1:a',
        # Video encoding
        '-c:v', VIDEO_CODEC,
        '-preset', VIDEO_PRESET,
        '-crf', str(VIDEO_CRF),
        # Audio encoding
        '-c:a', AUDIO_CODEC,
        '-b:a', AUDIO_BITRATE,
        # Output settings
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        '-shortest',
        str(output_path)
    ]

    log_info("Rendering Shorts video...")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        log_success(f"Shorts video rendered: {output_path}")
    except subprocess.CalledProcessError as e:
        log_error(f"FFmpeg failed: {e.stderr}")
        sys.exit(1)

    # Get output video info
    output_info = get_video_info(output_path)
    if 'error' not in output_info:
        width = output_info.get('width', 0)
        height = output_info.get('height', 0)
        out_duration = output_info.get('duration', 0)
        log_success(f"Output: {width}x{height}, {out_duration:.1f}s")

    # Summary
    click.echo("")
    click.echo(click.style("=" * 50, fg='green'))
    click.echo(click.style("SHORTS COMPLETE", fg='green', bold=True))
    click.echo(click.style("=" * 50, fg='green'))
    click.echo("")
    click.echo(f"Track:    {track_info.title}")
    click.echo(f"Segment:  {start} + {duration}s")
    if title:
        click.echo(f"Title:    {title}")
    if srt:
        click.echo(f"SRT:      {Path(srt).name} (dynamic)")
    elif lyric:
        click.echo(f"Lyric:    {lyric} (static)")
    click.echo(f"Output:   {output_path}")
    click.echo("")
    click.echo("Ready for YouTube Shorts upload!")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    cli()
