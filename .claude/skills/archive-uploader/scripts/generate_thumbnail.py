#!/usr/bin/env python3
"""
Generate thumbnail/cover images for archive.org uploads.

Usage:
    python generate_thumbnail.py <folder> [--output thumbnail.jpg]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# ============================================================
# Configuration
# ============================================================

TEMPLATES = {
    "islamic": {
        "bg_color": "#1a4d2e",      # Deep green
        "accent_color": "#c9a227",   # Gold
        "text_color": "#ffffff",     # White
        "subtitle_color": "#e8e8e8"  # Light gray
    },
    "modern": {
        "bg_color": "#2c3e50",       # Dark blue-gray
        "accent_color": "#3498db",   # Blue
        "text_color": "#ffffff",
        "subtitle_color": "#bdc3c7"
    },
    "minimal": {
        "bg_color": "#f5f5f5",       # Light gray
        "accent_color": "#333333",   # Dark gray
        "text_color": "#333333",
        "subtitle_color": "#666666"
    }
}

DEFAULT_TEMPLATE = "islamic"
IMAGE_SIZE = (1400, 1400)  # Square for archive.org


# ============================================================
# Helper Functions
# ============================================================

def extract_chapter_info(folder: Path) -> tuple[str, str]:
    """Extract chapter number and name from folder name."""
    name = folder.name
    chapter_num = ""
    chapter_name = name

    if "_" in name and name.split("_")[0].isdigit():
        chapter_num = name.split("_")[0]
        chapter_name = "_".join(name.split("_")[1:])

    if "(" in chapter_name:
        chapter_name = chapter_name.split("(")[0].strip()

    return chapter_num, chapter_name


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get a font, falling back to default if custom fonts not available."""
    font_names = [
        "arial.ttf", "Arial.ttf",
        "segoeui.ttf", "SegoeUI.ttf",
        "DejaVuSans.ttf",
        "LiberationSans-Regular.ttf"
    ]

    if bold:
        font_names = [
            "arialbd.ttf", "Arial Bold.ttf",
            "segoeuib.ttf", "SegoeUI-Bold.ttf",
            "DejaVuSans-Bold.ttf",
            "LiberationSans-Bold.ttf"
        ] + font_names

    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except (OSError, IOError):
            continue

    # Fallback to default
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines


# ============================================================
# Thumbnail Generation
# ============================================================

def generate_thumbnail(
    folder: Path,
    output_path: Path | None = None,
    template: str = DEFAULT_TEMPLATE,
    creator: str = "Sheikh Mohammad Mohsin",
    series: str = "Al Fiqh ul Ahwat"
) -> Path:
    """Generate a thumbnail image for the lecture series."""

    colors = TEMPLATES.get(template, TEMPLATES[DEFAULT_TEMPLATE])
    chapter_num, chapter_name = extract_chapter_info(folder)

    # Create image
    img = Image.new("RGB", IMAGE_SIZE, colors["bg_color"])
    draw = ImageDraw.Draw(img)

    # Get fonts
    title_font = get_font(90, bold=True)
    chapter_font = get_font(120, bold=True)
    subtitle_font = get_font(50)
    number_font = get_font(200, bold=True)

    # Calculate positions
    width, height = IMAGE_SIZE
    padding = 100
    max_text_width = width - (padding * 2)

    # Draw decorative top bar
    draw.rectangle([0, 0, width, 20], fill=colors["accent_color"])

    # Draw chapter number (large, top-right)
    if chapter_num:
        num_bbox = number_font.getbbox(chapter_num)
        num_width = num_bbox[2] - num_bbox[0]
        draw.text(
            (width - padding - num_width, 80),
            chapter_num,
            font=number_font,
            fill=colors["accent_color"]
        )

    # Draw series name (top)
    draw.text(
        (padding, 100),
        series.upper(),
        font=subtitle_font,
        fill=colors["subtitle_color"]
    )

    # Draw "Lecture Series" label
    draw.text(
        (padding, 160),
        "LECTURE SERIES",
        font=subtitle_font,
        fill=colors["accent_color"]
    )

    # Draw chapter name (center, wrapped)
    chapter_display = chapter_name.replace("-", " ")
    lines = wrap_text(chapter_display, chapter_font, max_text_width)

    # Calculate vertical center for chapter name
    line_height = 130
    total_text_height = len(lines) * line_height
    start_y = (height - total_text_height) // 2

    for i, line in enumerate(lines):
        y = start_y + (i * line_height)
        draw.text(
            (padding, y),
            line,
            font=chapter_font,
            fill=colors["text_color"]
        )

    # Draw creator name (bottom)
    draw.text(
        (padding, height - 180),
        f"By {creator}",
        font=title_font,
        fill=colors["subtitle_color"]
    )

    # Draw decorative bottom bar
    draw.rectangle([0, height - 20, width, height], fill=colors["accent_color"])

    # Determine output path
    if output_path is None:
        output_path = folder / "thumbnail.jpg"

    # Save image
    img.save(output_path, "JPEG", quality=95)
    print(f"Thumbnail saved: {output_path}")

    return output_path


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate thumbnail for archive.org upload"
    )
    parser.add_argument("folder", type=Path, help="Folder containing audio files")
    parser.add_argument("--output", "-o", type=Path, help="Output file path")
    parser.add_argument("--template", "-t", choices=list(TEMPLATES.keys()),
                        default=DEFAULT_TEMPLATE, help="Color template")
    parser.add_argument("--creator", default="Sheikh Mohammad Mohsin",
                        help="Creator name")
    parser.add_argument("--series", default="Al Fiqh ul Ahwat",
                        help="Series name")

    args = parser.parse_args()

    if not args.folder.is_dir():
        print(f"Error: {args.folder} is not a directory")
        sys.exit(1)

    generate_thumbnail(
        args.folder,
        args.output,
        args.template,
        args.creator,
        args.series
    )


if __name__ == "__main__":
    main()
