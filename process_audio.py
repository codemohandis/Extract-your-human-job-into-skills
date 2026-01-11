#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Audio Processing Pipeline

Imports and orchestrates the individual skills:
1. audio-metadata-editor: Edit ID3 tags
2. archive-uploader: Upload to archive.org

Usage:
    python process_audio.py <folder>                    # Process single folder
    python process_audio.py --all                       # Process all pending folders
    python process_audio.py <folder> --tag-only         # Only add metadata
    python process_audio.py <folder> --upload-only      # Only upload
    python process_audio.py <folder> --dry-run          # Preview without changes
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

# Fix for Windows console UTF-8 encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add skills to path for importing
SKILLS_PATH = Path(__file__).parent / ".claude" / "skills"
sys.path.insert(0, str(SKILLS_PATH / "audio-metadata-editor" / "scripts"))
sys.path.insert(0, str(SKILLS_PATH / "archive-uploader" / "scripts"))

# Import from skills (NO CODE DUPLICATION!)
from edit_metadata import process_folder as tag_folder
from upload_to_archive import (
    upload_to_archive,
    generate_identifier,
    generate_description,
    generate_tags,
    check_archive_exists,
    move_to_done,
    get_audio_files
)


# ============================================================
# Configuration
# ============================================================

def load_config() -> dict:
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {
        "defaults": {
            "artist": "Sheikh Mohammad Mohsin",
            "album": "Al Fiqh ul Ahwat Lecture Series",
            "genre": "Islamic Jurisprudence",
            "language": "Urdu",
            "collection": "opensource_audio",
            "base_tags": "Islamic Lecture; Fiqh; Urdu"
        },
        "folders": {
            "input": "audio_folders",
            "done": "audio-uploaded-done"
        }
    }


# ============================================================
# Upload History
# ============================================================

def get_history_path() -> Path:
    return Path(__file__).parent / "upload_history.json"


def load_history() -> dict:
    path = get_history_path()
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    path = get_history_path()
    with open(path, "w") as f:
        json.dump(history, f, indent=2)


def add_to_history(identifier: str, folder_name: str, url: str, file_count: int):
    history = load_history()
    history[identifier] = {
        "folder": folder_name,
        "uploaded": datetime.now().isoformat(),
        "url": url,
        "files": file_count
    }
    save_history(history)


def is_already_uploaded(identifier: str) -> bool:
    return identifier in load_history()


# ============================================================
# Pipeline Steps
# ============================================================

def step_tag_metadata(folder: Path, config: dict, dry_run: bool = False) -> bool:
    """Step 1: Edit metadata using audio-metadata-editor skill."""
    print("\n[STEP 1] Editing metadata...")

    if dry_run:
        print("  [DRY RUN] Would tag metadata")
        return True

    defaults = config["defaults"]
    success, skipped = tag_folder(
        folder,
        artist=defaults["artist"],
        album=defaults["album"],
        genre=defaults["genre"],
        language=defaults["language"]
    )

    return success > 0


def step_upload(folder: Path, config: dict, dry_run: bool = False, skip_thumbnail: bool = False) -> bool:
    """Step 2: Upload using archive-uploader skill."""
    print("\n[STEP 2] Uploading to archive.org...")

    defaults = config["defaults"]
    identifier = generate_identifier(folder)

    # Check for duplicates
    if is_already_uploaded(identifier):
        print(f"  [SKIP] Already in upload history: {identifier}")
        return False

    if check_archive_exists(identifier):
        print(f"  [SKIP] Already exists on archive.org: {identifier}")
        file_count = len(get_audio_files(folder))
        add_to_history(identifier, folder.name, f"https://archive.org/details/{identifier}", file_count)
        return False

    # Generate metadata
    description = generate_description(folder, defaults["artist"])
    tags = generate_tags(folder, defaults["base_tags"])

    # Upload (without auto-move, we'll handle it separately)
    success = upload_to_archive(
        folder=folder,
        identifier=None,  # Auto-generate
        creator=defaults["artist"],
        description=description,
        tags=tags,
        collection=defaults["collection"],
        dry_run=dry_run,
        auto_move=False,  # We handle move in step 3
        generate_cover=not skip_thumbnail
    )

    if success and not dry_run:
        file_count = len(get_audio_files(folder))
        add_to_history(identifier, folder.name, f"https://archive.org/details/{identifier}", file_count)

    return success


def step_move_to_done(folder: Path, config: dict, dry_run: bool = False) -> bool:
    """Step 3: Move folder to done directory."""
    print("\n[STEP 3] Moving to done folder...")

    done_folder = Path(__file__).parent / config["folders"]["done"]

    if dry_run:
        print(f"  [DRY RUN] Would move to: {done_folder / folder.name}")
        return True

    result = move_to_done(folder, done_folder)
    if result:
        print(f"  Moved to: {result}")
    return result is not None


# ============================================================
# Main Pipeline
# ============================================================

def process_folder(folder: Path, config: dict, tag_only: bool = False,
                   upload_only: bool = False, dry_run: bool = False, skip_thumbnail: bool = False) -> bool:
    """Process a single folder through the pipeline."""
    print("=" * 60)
    print(f"Processing: {folder.name}")
    print("=" * 60)

    if not folder.is_dir():
        print(f"Error: {folder} is not a directory")
        return False

    # Step 1: Edit metadata (unless upload-only)
    if not upload_only:
        if not step_tag_metadata(folder, config, dry_run):
            print("  Warning: Metadata step had issues")

    if tag_only:
        print("\n[DONE] Metadata updated (--tag-only mode)")
        return True

    # Step 2: Upload to archive.org
    if not step_upload(folder, config, dry_run, skip_thumbnail):
        return False

    # Step 3: Move to done folder
    if not dry_run:
        step_move_to_done(folder, config, dry_run)

    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    return True


def process_all(config: dict, dry_run: bool = False, skip_thumbnail: bool = False) -> int:
    """Process all folders in input directory."""
    input_folder = Path(__file__).parent / config["folders"]["input"]

    if not input_folder.exists():
        print(f"Input folder not found: {input_folder}")
        return 0

    folders = [f for f in input_folder.iterdir() if f.is_dir()]

    if not folders:
        print("No folders to process!")
        return 0

    print(f"Found {len(folders)} folders to process\n")

    success_count = 0
    for folder in sorted(folders):
        if process_folder(folder, config, dry_run=dry_run, skip_thumbnail=skip_thumbnail):
            success_count += 1
        print()

    print(f"\nProcessed {success_count}/{len(folders)} folders successfully")
    return success_count


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Unified Audio Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process_audio.py audio_folders/21_Chapter      # Process single folder
  python process_audio.py --all                         # Process all pending
  python process_audio.py folder --tag-only             # Only add metadata
  python process_audio.py folder --dry-run              # Preview changes
        """
    )
    parser.add_argument("folder", nargs="?", type=Path, help="Folder to process")
    parser.add_argument("--all", action="store_true", help="Process all folders in input directory")
    parser.add_argument("--tag-only", action="store_true", help="Only edit metadata, don't upload")
    parser.add_argument("--upload-only", action="store_true", help="Only upload, skip metadata")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    parser.add_argument("--skip-thumbnail", action="store_true", help="Skip thumbnail generation during upload")
    parser.add_argument("--history", action="store_true", help="Show upload history")

    args = parser.parse_args()
    config = load_config()

    # Show history
    if args.history:
        history = load_history()
        if not history:
            print("No upload history yet.")
        else:
            print("Upload History:")
            print("-" * 60)
            for identifier, info in history.items():
                print(f"  {identifier}")
                print(f"    Folder: {info['folder']}")
                print(f"    Date:   {info['uploaded']}")
                print(f"    Files:  {info['files']}")
                print(f"    URL:    {info['url']}")
                print()
        return

    # Process all folders
    if args.all:
        process_all(config, args.dry_run, args.skip_thumbnail)
        return

    # Process single folder
    if not args.folder:
        parser.print_help()
        sys.exit(1)

    process_folder(args.folder, config, args.tag_only, args.upload_only, args.dry_run, args.skip_thumbnail)


if __name__ == "__main__":
    main()
