#!/usr/bin/env python3
"""
Batch edit ID3 metadata for lecture audio files.

Usage:
    python edit_metadata.py <folder> --artist "Speaker Name" [--year 2024] [--copyright "License"]
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3, ID3NoHeaderError, TCOP, TLAN, COMM
    from mutagen.mp3 import MP3
except ImportError:
    print("Error: mutagen not installed. Run: pip install mutagen")
    sys.exit(1)

# Filename pattern: Chapter-Name_Dars XX.ext
FILENAME_PATTERN = re.compile(
    r"^(?P<chapter>.+?)_Dars\s+(?P<num>\d+)\.(?P<ext>mp3|m4a|wav)$",
    re.IGNORECASE
)


def parse_filename(filename: str) -> dict | None:
    """Parse chapter name and lecture number from filename."""
    match = FILENAME_PATTERN.match(filename)
    if not match:
        return None
    return {
        "chapter": match.group("chapter").replace("-", " "),
        "num": match.group("num").zfill(2),
        "ext": match.group("ext").lower()
    }


def edit_metadata(
    file_path: Path,
    chapter: str,
    lecture_num: str,
    artist: str,
    album: str = "Al Fiqh ul Ahwat Lecture Series",
    genre: str = "Islamic Jurisprudence",
    language: str = "Urdu",
    year: str | None = None,
    copyright_text: str | None = None
) -> bool:
    """Edit ID3 tags for a single audio file."""
    try:
        # Ensure file has ID3 tags (add empty ones if missing)
        try:
            audio = MP3(file_path)
            if audio.tags is None:
                audio.add_tags()
                audio.save()
        except Exception:
            pass

        # Use EasyID3 for common tags
        try:
            easy = EasyID3(file_path)
        except ID3NoHeaderError:
            # Create ID3 tags if they don't exist
            easy = EasyID3()
            easy.save(file_path)
            easy = EasyID3(file_path)

        title = chapter

        easy["title"] = title
        easy["tracknumber"] = lecture_num
        easy["artist"] = artist
        easy["album"] = album
        easy["albumartist"] = artist
        easy["genre"] = genre

        if year:
            easy["date"] = year

        easy.save()

        # Add tags not supported by EasyID3
        audio = ID3(file_path)
        audio.add(TLAN(encoding=3, text=[language]))
        audio.add(COMM(encoding=3, lang="eng", desc="", text=[chapter]))

        if copyright_text:
            audio.add(TCOP(encoding=3, text=[copyright_text]))

        audio.save()
        return True

    except Exception as e:
        print(f"  Error: {e}")
        return False


def process_folder(
    folder: Path,
    artist: str,
    album: str = "Al Fiqh ul Ahwat Lecture Series",
    genre: str = "Islamic Jurisprudence",
    language: str = "Urdu",
    year: str | None = None,
    copyright_text: str | None = None
) -> tuple[int, int]:
    """Process all matching audio files in folder."""
    success = 0
    skipped = 0

    audio_files = list(folder.glob("*.mp3")) + list(folder.glob("*.m4a"))

    if not audio_files:
        print(f"No audio files found in {folder}")
        return 0, 0

    print(f"Processing {len(audio_files)} files...\n")

    for file_path in sorted(audio_files):
        parsed = parse_filename(file_path.name)

        if not parsed:
            print(f"[SKIP] {file_path.name} - doesn't match pattern")
            skipped += 1
            continue

        print(f"[EDIT] {file_path.name}")
        print(f"       Title: {parsed['chapter']} - Dars {parsed['num']}")

        if edit_metadata(
            file_path,
            parsed["chapter"],
            parsed["num"],
            artist,
            album,
            genre,
            language,
            year,
            copyright_text
        ):
            success += 1
        else:
            skipped += 1

    return success, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Batch edit ID3 metadata for lecture audio files"
    )
    parser.add_argument("folder", type=Path, help="Folder containing audio files")
    parser.add_argument("--artist", required=True, help="Speaker/Artist name")
    parser.add_argument("--year", help="Year of recording")
    parser.add_argument("--copyright", dest="copyright_text", help="Copyright/License text")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    args = parser.parse_args()

    if not args.folder.is_dir():
        print(f"Error: {args.folder} is not a directory")
        sys.exit(1)

    print(f"Folder: {args.folder}")
    print(f"Artist: {args.artist}")
    if args.year:
        print(f"Year: {args.year}")
    if args.copyright_text:
        print(f"Copyright: {args.copyright_text}")
    print("-" * 50)

    if args.dry_run:
        print("\n[DRY RUN - No changes will be made]\n")
        for file_path in sorted(args.folder.glob("*.mp3")):
            parsed = parse_filename(file_path.name)
            if parsed:
                print(f"Would edit: {file_path.name}")
                print(f"  Title: {parsed['chapter']} - Dars {parsed['num']}")
            else:
                print(f"Would skip: {file_path.name} (doesn't match pattern)")
        sys.exit(0)

    success, skipped = process_folder(
        args.folder,
        args.artist,
        year=args.year,
        copyright_text=args.copyright_text
    )

    print("-" * 50)
    print(f"Done! Success: {success}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
