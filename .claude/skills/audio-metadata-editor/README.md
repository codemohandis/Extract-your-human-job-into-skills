# Audio Metadata Editor

Batch edit ID3 metadata tags for lecture audio files, preparing them for archive.org or other platforms.

## Overview

This skill adds standardized ID3 metadata tags to audio files, crucial for:
- Proper display in media players
- Archive.org library organization
- Search and discovery on platforms
- Professional presentation of content

## Features

- **Batch ID3 tagging** - Process entire folders at once
- **Flexible input** - Accepts various audio formats
- **Smart parsing** - Extracts info from standardized filenames
- **UTF-8 support** - Full Unicode support for Urdu/Arabic text
- **Zero-padding** - Ensures track numbers are zero-padded (01, 02, etc.)
- **Dry-run mode** - Preview changes before applying
- **Error recovery** - Continues on individual file errors
- **Comprehensive tags** - Handles 10+ ID3 tag fields

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# Required library
pip install mutagen
```

### Verify Installation

```bash
python -c "import mutagen; print('mutagen installed:', mutagen.__version__)"
```

## Usage

### Basic Usage

```bash
# Edit metadata for all audio files in folder
python scripts/edit_metadata.py <folder> --artist "Speaker Name"

# With optional fields
python scripts/edit_metadata.py <folder> \
  --artist "Sheikh Mohammad Mohsin" \
  --year 2024 \
  --copyright "Creative Commons Attribution"

# Preview without making changes
python scripts/edit_metadata.py <folder> --artist "Speaker Name" --dry-run
```

### Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `folder` | Yes | Path to folder containing audio files |
| `--artist` | Yes | Speaker/Artist name |
| `--year` | No | Year of recording (optional) |
| `--copyright` | No | Copyright/License text (optional) |
| `--dry-run` | No | Show changes without applying them |

### Examples

**Example 1: Basic metadata editing**
```bash
python scripts/edit_metadata.py audio_folders/21_Al-Shurb-e-Khamr \
  --artist "Sheikh Mohammad Mohsin"

# Output:
# Processing 2 files...
# [EDIT] Al-Shurb-e-Khamr_Dars 01.mp3
#        Title: Al Shurb e Khamr - Dars 01
# [EDIT] Al-Shurb-e-Khamr_Dars 02.mp3
#        Title: Al Shurb e Khamr - Dars 02
# Done! Success: 2, Skipped: 0
```

**Example 2: Complete metadata with year**
```bash
python scripts/edit_metadata.py audio_folders/22_Al-Murtad \
  --artist "Sheikh Mohammad Mohsin" \
  --year 2023 \
  --copyright "Public Domain"
```

**Example 3: Dry-run preview**
```bash
python scripts/edit_metadata.py audio_folders/21_Al-Shurb-e-Khamr \
  --artist "Sheikh Mohammad Mohsin" \
  --dry-run

# Shows what WOULD be edited without making changes
```

## File Name Requirements

### Expected Pattern

Files must follow this naming convention:

```
<Chapter-Name>_Dars <XX>.<ext>
```

**Valid Examples:**
- `Al-Eela_Dars 01.mp3`
- `Al-Shurb-e-Khamr_Dars 02.mp3`
- `Al-Murtad_Dars 03.mp3`
- `Chapter-Name_Dars 10.m4a`

**Invalid Examples (skipped):**
- `chapter-1.mp3` (missing "Dars" keyword)
- `Al-Eela.mp3` (missing lesson number)
- `Eela Dars 1.mp3` (missing underscore separator)

### Filename Parsing Regex

```regex
^(?P<chapter>.+?)_Dars\s+(?P<num>\d+)\.(?P<ext>mp3|m4a|wav)$
```

This matches:
- Chapter name: Any text before "_Dars"
- Separator: "_Dars " (underscore, word, space)
- Number: 1-3 digits
- Extension: .mp3, .m4a, or .wav

## ID3 Tag Mapping

The script sets the following ID3 metadata fields:

| ID3 Field | Value | Source |
|-----------|-------|--------|
| **Title** | Chapter Name | Extracted from filename (hyphens → spaces) |
| **Track Number** | Zero-padded lesson number | From filename (01, 02, etc.) |
| **Artist** | Speaker Name | User provided via `--artist` |
| **Album** | Al Fiqh ul Ahwat Lecture Series | Fixed/configurable |
| **Album Artist** | Speaker Name | Same as Artist |
| **Genre** | Islamic Jurisprudence | Fixed/configurable |
| **Language** | Urdu | Fixed |
| **Year** | User-provided year | From `--year` argument (optional) |
| **Comment** | Chapter Name | For reference in players |
| **Copyright** | User-provided text | From `--copyright` argument (optional) |

### Title Formatting

Chapter names are normalized for display:

```
Filename:  Al-Shurb-e-Khamr_Dars 01.mp3
Extracted: Al-Shurb-e-Khamr
Display:   Al Shurb e Khamr  (hyphens become spaces)
```

### Track Number Formatting

Numbers are zero-padded to 2 digits:

```
Input:  Dars 1   → Track: 01
Input:  Dars 5   → Track: 05
Input:  Dars 25  → Track: 25
```

## Supported Audio Formats

- `.mp3` - MPEG Audio (most common)
- `.m4a` - iTunes/Apple Audio
- `.wav` - Uncompressed Audio

Note: Other formats (.flac, .ogg) can be added by modifying the pattern regex.

## Error Handling

### Skipped Files

Files are skipped if they don't match the pattern:

```
[SKIP] unknown-file.mp3 - doesn't match pattern
[SKIP] Chapter 1.mp3 - doesn't match pattern
```

**Solution:** Rename files to match `<Chapter-Name>_Dars <XX>` pattern.

### Missing Mutagen Library

```
Error: mutagen not installed. Run: pip install mutagen
```

**Solution:**
```bash
pip install mutagen
```

### File Permission Error

```
[EDIT] file.mp3
Error: Permission denied
```

**Solutions:**
1. Close file in media player
2. Check file permissions: `chmod 644 file.mp3` (Linux/Mac)
3. Run as administrator (Windows)

### ID3 Tag Creation Issues

If files don't have ID3 headers, the script automatically:
1. Creates empty ID3 headers
2. Adds the metadata
3. Saves the file

This happens transparently - no special action needed.

## Advanced Usage

### Custom Album/Genre

Edit `scripts/edit_metadata.py` to change defaults:

```python
def process_folder(
    folder: Path,
    artist: str,
    album: str = "Your Custom Album Name",      # ← Change here
    genre: str = "Your Genre",                  # ← Change here
    ...
):
```

### Processing Multiple Folders

Script processes one folder at a time. For batch processing:

```bash
# Linux/Mac
for folder in audio_folders/*/; do
  python scripts/edit_metadata.py "$folder" --artist "Sheikh Name"
done

# Windows (PowerShell)
Get-ChildItem audio_folders -Directory | ForEach-Object {
  python scripts/edit_metadata.py $_.FullName --artist "Sheikh Name"
}
```

### Using with Pipeline

This skill is **Step 2** in the audio processing pipeline:

```
Step 1: Rename files & folders (urdu-audio-renamer)
         ↓
Step 2: Edit metadata tags (this skill)
         ↓
Step 3: Upload to archive.org (archive-uploader)
```

**Integrated pipeline command:**
```bash
python process_audio.py audio_folders/21_Chapter-Name
```

## Troubleshooting

### No Files Found

```
No audio files found in {folder}
```

**Causes:**
- Folder is empty
- Audio files are in subdirectories
- Files have unsupported extensions

**Solutions:**
1. Check folder path: `ls /path/to/folder`
2. Files must be directly in folder (not in subfolders)
3. Use supported formats: .mp3, .m4a, .wav

### Files Not Being Edited

**Problem:** Files appear as [SKIP] even though they should match.

**Solution:** Check filename format:

```
✓ Correct format:  Al-Eela_Dars 01.mp3
✗ Missing Dars:    Al-Eela_01.mp3
✗ Wrong separator: Al-Eela-Dars 01.mp3
✗ Missing number:  Al-Eela_Dars.mp3
```

### Tags Not Visible in Player

**Problem:** Tags edited but don't appear in media player.

**Solution:**
1. Refresh player library: Close and reopen
2. Clear player cache (depends on media player)
3. Use different player to verify: VLC, foobar2000, etc.

### Dry-Run Shows Wrong Info

**Problem:** Preview shows incorrect title/track info.

**Solution:** Check filename matches pattern. Dry-run parses filenames the same way as actual edit.

## Integration Points

### With Archive Uploader

After editing metadata, upload with archive-uploader skill:

```bash
# Step 1: Rename
python scripts/rename_audio.py folder

# Step 2: Edit metadata
python scripts/edit_metadata.py folder --artist "Speaker Name"

# Step 3: Upload
python scripts/upload_to_archive.py folder --creator "Speaker Name" \
  --description "Description" --tags "tag1; tag2"
```

### With Config File

The main pipeline reads from `config.yaml`:

```yaml
defaults:
  artist: "Sheikh Mohammad Mohsin"
  album: "Al Fiqh ul Ahwat Lecture Series"
  genre: "Islamic Jurisprudence"
```

## API Reference

### Main Functions

```python
def parse_filename(filename: str) -> dict | None:
    """
    Parse filename to extract chapter name and lecture number.
    Returns: {"chapter": str, "num": str, "ext": str} or None
    """

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
    """
    Edit ID3 tags for a single audio file.
    Returns: True if successful, False if failed
    """

def process_folder(
    folder: Path,
    artist: str,
    album: str = "Al Fiqh ul Ahwat Lecture Series",
    genre: str = "Islamic Jurisprudence",
    language: str = "Urdu",
    year: str | None = None,
    copyright_text: str | None = None
) -> tuple[int, int]:
    """
    Process all matching audio files in folder.
    Returns: (success_count, skipped_count)
    """
```

## Performance

- **Processing speed:** ~100 files/minute (depends on file size and disk speed)
- **Memory usage:** Minimal (~10 MB)
- **Disk I/O:** Sequential reads/writes

## Encoding & Internationalization

- ✓ Full UTF-8 support for all text fields
- ✓ Handles Urdu, Arabic, English text in metadata
- ✓ Windows console encoding fixes included
- ✓ Cross-platform compatible (Windows, Linux, macOS)

## References

- [ID3v2 Tag Structure](https://id3.org/id3v2.4.0-structure) - Technical specification
- [Mutagen Documentation](https://mutagen.readthedocs.io/) - Library documentation

## License

Part of the "Extract Your Human Job Into Skills" project.

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Verify filename pattern matches expected format
3. Ensure mutagen library is installed
4. Consult project documentation in `CLAUDE.md`
