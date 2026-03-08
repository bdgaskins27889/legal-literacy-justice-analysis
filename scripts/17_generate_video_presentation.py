"""
Script: 17_generate_video_presentation.py
Purpose: Render each slide HTML to PNG, pair with narration audio,
         and combine into a single polished MP4 video presentation.
Author:  Barbara D. Gaskins
Project: The Scales of Justice — DSC 680 Capstone, March 2026
"""

import os
import subprocess
import glob
import json
import shutil
from pathlib import Path
from pydub import AudioSegment

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_DIR  = Path("/home/ubuntu/legal_literacy_justice_project")
SLIDES_DIR   = PROJECT_DIR / "slides_project"
AUDIO_DIR    = PROJECT_DIR / "outputs" / "audio"
VIDEO_DIR    = PROJECT_DIR / "outputs" / "video"
FRAMES_DIR   = VIDEO_DIR / "frames"

VIDEO_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# ── Slide order (matches slide_state.json pageNum order) ─────────────────────
SLIDE_ORDER = [
    ("slide_1_title",                "slide_01_title.mp3"),
    ("slide_2_central_question",     "slide_02_central_question.mp3"),
    ("slide_3_dataset",              "slide_03_dataset.mp3"),
    ("slide_4_conceptual_framework", "slide_04_conceptual_framework.mp3"),
    ("slide_5_finding_1",            "slide_05_finding_racial_disparities.mp3"),
    ("slide_6_finding_2",            "slide_06_finding_representation_gap.mp3"),
    ("slide_7_methodology",          "slide_07_methodology.mp3"),
    ("slide_8_model_performance",    "slide_08_model_performance.mp3"),
    ("slide_9_model_fairness",       "slide_09_fairness_analysis.mp3"),
    ("slide_10_why_fairer",          "slide_10_why_fairer.mp3"),
    ("slide_11_discussion",          "slide_11_discussion.mp3"),
    ("slide_12_policy_implications", "slide_12_policy_implications.mp3"),
    ("slide_13_limitations",         "slide_13_limitations.mp3"),
    ("slide_14_conclusion",          "slide_14_conclusion.mp3"),
    ("slide_15_qa",                  "slide_15_qa.mp3"),
    ("slide_16_references",          "slide_16_references.mp3"),
]

# ── Video settings ─────────────────────────────────────────────────────────────
WIDTH  = 1280
HEIGHT = 720
FPS    = 24
PAUSE_BETWEEN_SLIDES_MS = 800   # 0.8s silence between slides


def render_slide_to_png(slide_id: str, output_png: Path) -> bool:
    """Render an HTML slide to PNG using headless Chromium."""
    html_path = SLIDES_DIR / f"{slide_id}.html"
    if not html_path.exists():
        print(f"  ✗ HTML not found: {html_path}")
        return False

    cmd = [
        "chromium-browser",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        f"--window-size={WIDTH},{HEIGHT}",
        f"--screenshot={output_png}",
        f"file://{html_path}"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if output_png.exists() and output_png.stat().st_size > 1000:
        return True
    else:
        print(f"  ✗ Render failed for {slide_id}: {result.stderr[:200]}")
        return False


def get_audio_duration_ms(audio_path: Path) -> int:
    """Return audio duration in milliseconds."""
    seg = AudioSegment.from_mp3(str(audio_path))
    return len(seg)


def build_slide_video_segment(slide_png: Path, audio_mp3: Path,
                               output_mp4: Path, pause_ms: int = 800):
    """
    Create a video segment for one slide:
    - Image displayed for the full duration of the audio + pause
    - Audio plays, then silence for the pause duration
    """
    audio_dur_ms = get_audio_duration_ms(audio_mp3)
    total_dur_ms = audio_dur_ms + pause_ms
    total_dur_s  = total_dur_ms / 1000.0

    # Build padded audio (narration + silence)
    audio_seg  = AudioSegment.from_mp3(str(audio_mp3))
    silence    = AudioSegment.silent(duration=pause_ms)
    padded_audio = audio_seg + silence

    padded_audio_path = output_mp4.parent / f"{output_mp4.stem}_audio.mp3"
    padded_audio.export(str(padded_audio_path), format="mp3", bitrate="128k")

    # FFmpeg: loop image for total_dur_s, overlay audio, encode to H.264
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(slide_png),
        "-i", str(padded_audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-t", str(total_dur_s),
        "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
               f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:black",
        "-shortest",
        str(output_mp4)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    # Clean up temp audio
    if padded_audio_path.exists():
        padded_audio_path.unlink()

    if output_mp4.exists() and output_mp4.stat().st_size > 1000:
        return True
    else:
        print(f"  ✗ FFmpeg error: {result.stderr[-300:]}")
        return False


def concatenate_segments(segment_files: list, output_path: Path):
    """Concatenate all segment MP4 files into the final video."""
    concat_list = VIDEO_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",   # optimise for web streaming
        str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    concat_list.unlink(missing_ok=True)

    if output_path.exists() and output_path.stat().st_size > 10000:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Final video: {output_path.name} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  ✗ Concatenation failed: {result.stderr[-400:]}")
        return False


def add_title_card(output_mp4: Path):
    """Add a 2-second black fade-in at the start and fade-out at the end."""
    temp = output_mp4.parent / f"_temp_{output_mp4.name}"
    output_mp4.rename(temp)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp),
        "-vf", "fade=t=in:st=0:d=1,fade=t=out:st=0:d=1:eval=frame",
        "-af", "afade=t=in:st=0:d=1",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_mp4)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    temp.unlink(missing_ok=True)
    return output_mp4.exists()


def main():
    print("=" * 65)
    print("  THE SCALES OF JUSTICE — VIDEO PRESENTATION BUILDER")
    print("  Barbara D. Gaskins | DSC 680 Capstone | March 2026")
    print("=" * 65)
    print(f"\n  Resolution : {WIDTH}x{HEIGHT} @ {FPS}fps")
    print(f"  Slides     : {len(SLIDE_ORDER)}")
    print(f"  Output dir : {VIDEO_DIR}\n")

    # ── Step 1: Render all slides to PNG ──────────────────────────────────────
    print("STEP 1: Rendering slides to PNG images")
    print("-" * 65)
    slide_pngs = {}
    for i, (slide_id, _) in enumerate(SLIDE_ORDER, 1):
        png_path = FRAMES_DIR / f"{i:02d}_{slide_id}.png"
        print(f"  [{i:02d}/16] Rendering {slide_id}...")
        success = render_slide_to_png(slide_id, png_path)
        if success:
            size_kb = png_path.stat().st_size / 1024
            print(f"         ✓ {png_path.name} ({size_kb:.0f} KB)")
            slide_pngs[slide_id] = png_path
        else:
            print(f"         ✗ FAILED — using fallback black frame")
            # Create a plain black fallback PNG
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new("RGB", (WIDTH, HEIGHT), color=(26, 26, 26))
            draw = ImageDraw.Draw(img)
            draw.text((WIDTH//2 - 200, HEIGHT//2 - 20),
                      f"Slide {i}: {slide_id}", fill=(255, 255, 255))
            img.save(str(png_path))
            slide_pngs[slide_id] = png_path

    print(f"\n  ✓ All {len(slide_pngs)} slides rendered.\n")

    # ── Step 2: Build per-slide video segments ────────────────────────────────
    print("STEP 2: Building per-slide video segments")
    print("-" * 65)
    segment_files = []

    for i, (slide_id, audio_file) in enumerate(SLIDE_ORDER, 1):
        png_path   = slide_pngs[slide_id]
        audio_path = AUDIO_DIR / audio_file
        seg_output = VIDEO_DIR / f"seg_{i:02d}_{slide_id}.mp4"

        audio_dur = get_audio_duration_ms(audio_path) / 1000
        print(f"  [{i:02d}/16] {slide_id} ({audio_dur:.1f}s)...")

        success = build_slide_video_segment(
            png_path, audio_path, seg_output,
            pause_ms=PAUSE_BETWEEN_SLIDES_MS
        )
        if success:
            size_kb = seg_output.stat().st_size / 1024
            print(f"         ✓ Segment created ({size_kb:.0f} KB)")
            segment_files.append(seg_output)
        else:
            print(f"         ✗ Segment FAILED for slide {i}")

    print(f"\n  ✓ {len(segment_files)}/{len(SLIDE_ORDER)} segments built.\n")

    # ── Step 3: Concatenate all segments ──────────────────────────────────────
    print("STEP 3: Concatenating all segments into final video")
    print("-" * 65)
    final_output = VIDEO_DIR / "Scales_of_Justice_Presentation_Gaskins.mp4"
    success = concatenate_segments(segment_files, final_output)

    if not success:
        print("  ✗ Concatenation failed. Exiting.")
        return

    # ── Step 4: Get final video info ──────────────────────────────────────────
    print("\nSTEP 4: Final video metadata")
    print("-" * 65)
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", str(final_output)],
        capture_output=True, text=True
    )
    try:
        info = json.loads(probe.stdout)
        duration = float(info["format"]["duration"])
        size_mb  = float(info["format"]["size"]) / (1024 * 1024)
        print(f"  Duration  : {duration/60:.1f} minutes ({duration:.0f} seconds)")
        print(f"  File size : {size_mb:.1f} MB")
        print(f"  Format    : MP4 (H.264 video + AAC audio)")
        print(f"  Resolution: {WIDTH}x{HEIGHT}")
    except Exception:
        pass

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  VIDEO PRESENTATION COMPLETE")
    print("=" * 65)
    print(f"\n  Output: {final_output}")
    print("\n  Ready for Milestone 3 submission.\n")


if __name__ == "__main__":
    main()
