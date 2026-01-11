#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Thumbnail Generator for Archive.org

Generate cover images for Islamic lecture collections.
Run this SEPARATELY before uploading if desired.

Usage:
    python generate_thumbnail_standalone.py <folder>
    python generate_thumbnail_standalone.py <folder> --output custom-name.jpg
    python generate_thumbnail_standalone.py <folder> --template islamic
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed.")
    print("Install with: pip install Pillow")
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


def get_font(size: int, bold: bool = False):
    """Get a font, falling back to default if system fonts unavailable."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except (FileNotFoundError, OSError):
            continue

    # Fallback to default font
    return ImageFont.load_default()


def generate_thumbnail(
    folder: Path,
    creator: str = "Sheikh Mohammad Mohsin",
    template: str = DEFAULT_TEMPLATE,
    output_name: str = "thumbnail.jpg"
) -> Path:
    """
    Generate thumbnail image for archive.org upload.

    Args:
        folder: Path to audio folder
        creator: Speaker/creator name
        template: Color template (islamic, modern, minimal)
        output_name: Output filename

    Returns:
        Path to generated thumbnail
    """
    if template not in TEMPLATES:
        print(f"Warning: Unknown template '{template}'. Using default.")
        template = DEFAULT_TEMPLATE

    colors = TEMPLATES[template]
    chapter_num, chapter_name = extract_chapter_info(folder)

    # Create image
    img = Image.new("RGB", IMAGE_SIZE, colors["bg_color"])
    draw = ImageDraw.Draw(img)

    # Draw accent line
    line_height = IMAGE_SIZE[1] // 3
    draw.rectangle(
        [(0, line_height), (IMAGE_SIZE[0], line_height + 50)],
        fill=colors["accent_color"]
    )

    # Title fonts
    title_font = get_font(80, bold=True)
    subtitle_font = get_font(40)
    text_font = get_font(35)

    # Draw chapter number
    if chapter_num:
        num_text = f"Chapter {chapter_num}"
        bbox = draw.textbbox((0, 0), num_text, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (IMAGE_SIZE[0] - text_width) // 2
        draw.text(
            (x, 150),
            num_text,
            fill=colors["accent_color"],
            font=subtitle_font
        )

    # Draw chapter name
    # Handle long chapter names with wrapping
    chapter_display = chapter_name.replace("-", " ")
    lines = []
    words = chapter_display.split()

    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        text_width = bbox[2] - bbox[0]

        if text_width > IMAGE_SIZE[0] - 100 and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line)

    # Draw chapter name (centered)
    y_pos = line_height + 100
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (IMAGE_SIZE[0] - text_width) // 2
        draw.text(
            (x, y_pos),
            line,
            fill=colors["text_color"],
            font=title_font
        )
        y_pos += 120

    # Draw series info
    series_text = "Al Fiqh ul Ahwat Lecture Series"
    bbox = draw.textbbox((0, 0), series_text, font=subtitle_font)
    text_width = bbox[2] - bbox[0]
    x = (IMAGE_SIZE[0] - text_width) // 2
    draw.text(
        (x, IMAGE_SIZE[1] - 350),
        series_text,
        fill=colors["subtitle_color"],
        font=subtitle_font
    )

    # Draw creator name
    creator_text = f"by {creator}"
    bbox = draw.textbbox((0, 0), creator_text, font=text_font)
    text_width = bbox[2] - bbox[0]
    x = (IMAGE_SIZE[0] - text_width) // 2
    draw.text(
        (x, IMAGE_SIZE[1] - 200),
        creator_text,
        fill=colors["subtitle_color"],
        font=text_font
    )

    # Save thumbnail
    output_path = folder / output_name
    img.save(output_path, "JPEG", quality=95)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate thumbnail images for archive.org uploads",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_thumbnail_standalone.py audio_folders/21_Al-Shurb-e-Khamr
  python generate_thumbnail_standalone.py audio_folders/21_Al-Shurb-e-Khamr --template modern
  python generate_thumbnail_standalone.py audio_folders/21_Al-Shurb-e-Khamr --output cover.jpg
        """
    )

    parser.add_argument("folder", type=Path, help="Folder to generate thumbnail for")
    parser.add_argument(
        "--creator",
        default="Sheikh Mohammad Mohsin",
        help="Creator/speaker name (default: Sheikh Mohammad Mohsin)"
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE,
        choices=list(TEMPLATES.keys()),
        help=f"Color template (default: {DEFAULT_TEMPLATE})"
    )
    parser.add_argument(
        "--output",
        default="thumbnail.jpg",
        help="Output filename (default: thumbnail.jpg)"
    )

    args = parser.parse_args()

    if not args.folder.is_dir():
        print(f"Error: {args.folder} is not a directory")
        sys.exit(1)

    print(f"Generating thumbnail for: {args.folder.name}")
    print(f"Template: {args.template}")
    print(f"Creator: {args.creator}")

    try:
        output_path = generate_thumbnail(
            args.folder,
            creator=args.creator,
            template=args.template,
            output_name=args.output
        )
        print(f"✓ Thumbnail created: {output_path}")
        print(f"  You can now upload this folder to archive.org")
    except Exception as e:
        print(f"Error: Could not generate thumbnail: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
