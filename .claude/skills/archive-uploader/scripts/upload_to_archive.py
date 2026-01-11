#!/usr/bin/env python3
"""
Upload audio files to archive.org with metadata.

Usage:
    python upload_to_archive.py <folder> --identifier "item-id" --creator "Name" \
        --description "Description" --tags "tag1; tag2"
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    import internetarchive as ia
except ImportError:
    print("Error: internetarchive not installed. Run: pip install internetarchive")
    sys.exit(1)


# ============================================================
# Checkpointing System
# ============================================================

def get_checkpoint_path(identifier: str) -> Path:
    """Get checkpoint file path for an identifier."""
    checkpoint_dir = Path(__file__).parent.parent.parent.parent.parent / ".upload_checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    return checkpoint_dir / f"{identifier}.json"


def load_checkpoint(identifier: str) -> dict:
    """Load checkpoint for an upload."""
    path = get_checkpoint_path(identifier)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"uploaded_files": [], "failed_files": []}


def save_checkpoint(identifier: str, checkpoint: dict):
    """Save checkpoint after each file upload."""
    path = get_checkpoint_path(identifier)
    with open(path, "w") as f:
        json.dump(checkpoint, f, indent=2)


def clear_checkpoint(identifier: str):
    """Remove checkpoint file after successful upload."""
    path = get_checkpoint_path(identifier)
    if path.exists():
        path.unlink()


def get_audio_files(folder: Path) -> list[Path]:
    """Get all audio files from folder."""
    extensions = [".mp3", ".m4a", ".wav", ".flac", ".ogg"]
    files = []
    for ext in extensions:
        files.extend(folder.glob(f"*{ext}"))
    return sorted(files)


def extract_chapter_info(folder: Path) -> tuple[str, str]:
    """Extract chapter number and name from folder name.

    Returns: (chapter_num, chapter_name)
    """
    name = folder.name
    chapter_num = ""
    chapter_name = name

    # Extract leading number prefix like "21_"
    if "_" in name and name.split("_")[0].isdigit():
        chapter_num = name.split("_")[0]
        chapter_name = "_".join(name.split("_")[1:])

    # Remove lecture count suffix like "(02)"
    if "(" in chapter_name:
        chapter_name = chapter_name.split("(")[0].strip()

    return chapter_num, chapter_name


def generate_title(folder: Path) -> str:
    """Generate title: {chap_no} {Chapter Name} Lecture Series."""
    chapter_num, chapter_name = extract_chapter_info(folder)
    # Replace hyphens with spaces for display
    chapter_display = chapter_name.replace("-", " ")
    if chapter_num:
        return f"{chapter_num} {chapter_display} Lecture Series"
    return f"{chapter_display} Lecture Series"


def transliterate_urdu(text: str) -> str:
    """Transliterate Urdu/Arabic text to Roman characters for identifiers."""
    # Common Urdu/Arabic words in Islamic texts
    urdu_map = {
        "باب": "bab",
        "قصاص": "qisas",
        "درس": "dars",
        "کتاب": "kitab",
        "الصلاۃ": "al-salat",
        "الزکاۃ": "al-zakat",
        "الحج": "al-hajj",
        "الصوم": "al-sawm",
        "الجہاد": "al-jihad",
        "النکاح": "al-nikah",
        "الطلاق": "al-talaq",
        "البیع": "al-bay",
        "الایلاء": "al-ila",
        "الظہار": "al-zihar",
        "اللعان": "al-lian",
        "العدۃ": "al-iddat",
        "الرضاع": "al-riza",
        "النفقات": "al-nafaqat",
        "الحدود": "al-hudud",
        "القضاء": "al-qaza",
        "الشہادات": "al-shahadat",
        "الوصیۃ": "al-wasiyyat",
        "الفرائض": "al-faraiz",
        "الوقف": "al-waqf",
        "المرتد": "al-murtad",
        "الشرب": "al-shurb",
        "خمر": "khamr",
    }

    result = text
    for urdu, roman in urdu_map.items():
        result = result.replace(urdu, roman)

    # Remove any remaining non-ASCII characters
    result = ''.join(c if c.isascii() else '' for c in result)

    # Clean up multiple hyphens/spaces
    result = '-'.join(filter(None, result.replace(' ', '-').split('-')))

    return result.lower()


def generate_identifier(folder: Path) -> str:
    """Generate identifier: {chapter-name}-lecture-series (no chapter number)."""
    chapter_num, chapter_name = extract_chapter_info(folder)

    # Transliterate Urdu/Arabic to Roman
    identifier = transliterate_urdu(chapter_name)

    # If transliteration resulted in empty string, use folder name with number
    if not identifier or len(identifier) < 3:
        identifier = f"chapter-{chapter_num}" if chapter_num else "untitled"

    # Add chapter number if present
    if chapter_num:
        identifier = f"{chapter_num}-{identifier}"

    # Ensure valid identifier format
    identifier = identifier.lower().replace(" ", "-")
    identifier = '-'.join(filter(None, identifier.split('-')))  # Remove empty parts

    return f"{identifier}-lecture-series"


def generate_description(folder: Path, creator: str) -> str:
    """Generate description for archive.org."""
    _, chapter_name = extract_chapter_info(folder)
    chapter_display = chapter_name.replace("-", " ")
    file_count = len(get_audio_files(folder))
    return (
        f"{chapter_display} - Islamic Fiqh lecture series by {creator}. "
        f"Part of Al Fiqh ul Ahwat course. "
        f"Contains {file_count} lectures in Urdu."
    )


def generate_tags(folder: Path, base_tags: str = "Islamic Lecture; Fiqh; Urdu") -> str:
    """Generate tags for archive.org."""
    _, chapter_name = extract_chapter_info(folder)
    chapter_display = chapter_name.replace("-", " ")
    return f"{base_tags}; {chapter_display}"


def check_archive_exists(identifier: str) -> bool:
    """Check if item already exists on archive.org."""
    try:
        item = ia.get_item(identifier)
        return item.exists
    except Exception:
        return False


def move_to_done(folder: Path, done_folder: Path | None = None) -> Path | None:
    """Move folder to done directory after successful upload."""
    if done_folder is None:
        # Default: sibling to audio_folders
        parent = folder.parent.parent
        done_folder = parent / "audio-uploaded-done"

    # Create done folder if it doesn't exist
    done_folder.mkdir(exist_ok=True)

    destination = done_folder / folder.name

    try:
        shutil.move(str(folder), str(destination))
        return destination
    except Exception as e:
        print(f"Warning: Could not move folder: {e}")
        return None


def upload_to_archive(
    folder: Path,
    identifier: str | None,
    creator: str,
    description: str,
    tags: str,
    collection: str = "opensource_audio",
    dry_run: bool = False,
    auto_move: bool = True,
    done_folder: Path | None = None,
    generate_cover: bool = True
) -> bool:
    """Upload folder contents to archive.org with checkpointing support."""

    audio_files = get_audio_files(folder)

    if not audio_files:
        print(f"No audio files found in {folder}")
        return False

    title = generate_title(folder)

    # Auto-generate identifier if not provided
    if not identifier:
        identifier = generate_identifier(folder)

    # Load checkpoint to check for resume
    checkpoint = load_checkpoint(identifier)
    uploaded_files = set(checkpoint.get("uploaded_files", []))

    # Filter out already uploaded files
    files_to_upload = [f for f in audio_files if f.name not in uploaded_files]

    if uploaded_files:
        print(f"\n[RESUME] Found checkpoint: {len(uploaded_files)} files already uploaded")
        print(f"[RESUME] Remaining files: {len(files_to_upload)}")

    # Build metadata
    metadata = {
        "collection": collection,
        "mediatype": "audio",
        "title": title,
        "creator": creator,
        "description": description,
        "subject": tags,
        "language": "Urdu",
    }

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Upload Summary")
    print("=" * 50)
    print(f"Identifier: {identifier}")
    print(f"Title:      {title}")
    print(f"Creator:    {creator}")
    print(f"Collection: {collection}")
    print(f"Tags:       {tags}")
    print(f"Files:      {len(audio_files)} total, {len(files_to_upload)} to upload")
    print("-" * 50)
    print("Description:")
    print(description)
    print("-" * 50)
    print("Files to upload:")
    for f in files_to_upload:
        print(f"  - {f.name}")
    if uploaded_files:
        print(f"\nAlready uploaded ({len(uploaded_files)} files):")
        for name in sorted(uploaded_files)[:5]:
            print(f"  ✓ {name}")
        if len(uploaded_files) > 5:
            print(f"  ... and {len(uploaded_files) - 5} more")
    print("=" * 50)

    if dry_run:
        print("\n[DRY RUN] No files uploaded.")
        return True

    if not files_to_upload:
        print("\nAll files already uploaded!")
        clear_checkpoint(identifier)
        return True

    # Generate thumbnail if enabled
    thumbnail_path = None
    if generate_cover and "thumbnail.jpg" not in uploaded_files:
        try:
            from generate_thumbnail import generate_thumbnail as gen_thumb
            print("\nGenerating cover image...")
            thumbnail_path = gen_thumb(folder, creator=creator)
            files_to_upload.insert(0, thumbnail_path)  # Upload thumbnail first
        except ImportError:
            print("  [SKIP] Thumbnail generation not available (install Pillow)")
        except Exception as e:
            print(f"  [WARN] Could not generate thumbnail: {e}")

    # Upload files one by one with checkpointing
    print("\nUploading...")
    failed_files = []

    for i, audio_file in enumerate(files_to_upload, 1):
        print(f"\n[{i}/{len(files_to_upload)}] Uploading: {audio_file.name}")
        try:
            # Upload single file (metadata only needed for first file or new item)
            file_metadata = metadata if i == 1 and not uploaded_files else None

            responses = ia.upload(
                identifier,
                files=[str(audio_file)],
                metadata=file_metadata,
                verbose=True
            )

            # Check response
            if all(r.status_code == 200 for r in responses):
                print(f"  ✓ Success")
                uploaded_files.add(audio_file.name)
                # Save checkpoint after each successful upload
                save_checkpoint(identifier, {
                    "uploaded_files": list(uploaded_files),
                    "failed_files": failed_files
                })
            else:
                print(f"  ✗ Failed (status: {[r.status_code for r in responses]})")
                failed_files.append(audio_file.name)

        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed_files.append(audio_file.name)
            # Save checkpoint on failure
            save_checkpoint(identifier, {
                "uploaded_files": list(uploaded_files),
                "failed_files": failed_files
            })
            print(f"\n[CHECKPOINT] Progress saved. Run again to resume from file {i}.")
            return False

    # Check if all files uploaded successfully
    success = len(failed_files) == 0

    if success:
        # Clear checkpoint on complete success
        clear_checkpoint(identifier)
        print("\n" + "=" * 50)
        print("Upload complete!")
        print(f"URL: https://archive.org/details/{identifier}")

        # Move folder to done (if enabled)
        if auto_move:
            new_location = move_to_done(folder, done_folder)
            if new_location:
                print(f"Moved to: {new_location}")

        print("=" * 50)
        return True
    else:
        print(f"\n{len(failed_files)} files failed to upload.")
        print("Run again to retry failed files.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Upload audio files to archive.org"
    )
    parser.add_argument("folder", type=Path, help="Folder containing audio files")
    parser.add_argument("--identifier",
                       help="Unique item identifier (auto-generated if not provided)")
    parser.add_argument("--creator", required=True, help="Creator/Speaker name")
    parser.add_argument("--description", required=True, help="Item description")
    parser.add_argument("--tags", required=True,
                       help="Tags/subjects (semicolon-separated)")
    parser.add_argument("--collection", default="opensource_audio",
                       help="Target collection (default: opensource_audio)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be uploaded without uploading")
    parser.add_argument("--skip-thumbnail", action="store_true",
                       help="Skip thumbnail generation and upload")

    args = parser.parse_args()

    if not args.folder.is_dir():
        print(f"Error: {args.folder} is not a directory")
        sys.exit(1)

    # Validate identifier if provided (lowercase, hyphens, numbers only)
    if args.identifier and not all(c.islower() or c.isdigit() or c == "-" for c in args.identifier):
        print("Error: Identifier must be lowercase letters, numbers, and hyphens only")
        sys.exit(1)

    success = upload_to_archive(
        args.folder,
        args.identifier,
        args.creator,
        args.description,
        args.tags,
        args.collection,
        args.dry_run,
        generate_cover=not args.skip_thumbnail
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
