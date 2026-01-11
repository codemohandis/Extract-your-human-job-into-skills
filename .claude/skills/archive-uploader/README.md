# Archive.org Uploader

Batch upload audio files to archive.org with auto-generated metadata and intelligent checkpointing for reliable resumable uploads.

## Overview

This skill automates uploading Islamic lecture audio collections to Internet Archive (archive.org), including:
- Intelligent metadata generation from folder/file names
- Automatic thumbnail/cover image creation
- Resumable uploads with checkpoint system
- Duplicate detection to prevent re-uploading
- Automatic folder organization after successful upload

## Features

- **Batch uploads** - Upload entire folders to archive.org
- **Smart metadata** - Auto-generate title, description, and tags
- **Checkpointing** - Resume failed uploads from where they stopped
- **Duplicate detection** - Skip already-uploaded items
- **Cover generation** - Auto-create thumbnail for archive.org
- **URL formatting** - Proper identifier generation for archive.org URLs
- **Auto-move** - Move completed folders to done directory
- **Dry-run mode** - Preview uploads without uploading
- **Error recovery** - Detailed error messages and recovery instructions

## Prerequisites

### Archive.org Account

1. Create account: https://archive.org/account/signup
2. Enable S3 API: https://archive.org/account/s3.php
3. Generate API credentials

### Install Dependencies

```bash
pip install internetarchive pillow pyyaml
```

### Configure Archive.org Credentials

One-time setup:

```bash
ia configure
```

This will prompt for:
- Email address
- API access key
- API secret key

Credentials are saved to `~/.config/ia/credentials.txt`

### Verify Setup

```bash
ia list --help  # If this works, you're configured correctly
```

## Usage

### Basic Upload

```bash
# Upload folder with required metadata
python scripts/upload_to_archive.py <folder> \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "tag1; tag2; tag3"

# Auto-generate identifier
# Example: 21_al-shurb-e-khamr-lecture-series
```

### With Optional Arguments

```bash
# Specify custom identifier
python scripts/upload_to_archive.py <folder> \
  --identifier "custom-item-name" \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "Islamic Lecture; Fiqh; Urdu"

# Different collection (default: opensource_audio)
python scripts/upload_to_archive.py <folder> \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "tags" \
  --collection "my_collection"

# Dry-run (preview without uploading)
python scripts/upload_to_archive.py <folder> \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "tags" \
  --dry-run
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `folder` | Yes | - | Path to folder with audio files |
| `--identifier` | No | Auto-generated | archive.org item identifier |
| `--creator` | Yes | - | Speaker/Creator name |
| `--description` | Yes | - | Item description |
| `--tags` | Yes | - | Semicolon-separated tags |
| `--collection` | No | `opensource_audio` | Archive.org collection |
| `--dry-run` | No | False | Preview without uploading |

## Examples

### Example 1: Basic Upload

```bash
python scripts/upload_to_archive.py audio_folders/21_Al-Shurb-e-Khamr \
  --creator "Sheikh Mohammad Mohsin" \
  --description "Al Shurb e Khamr lecture series on Islamic jurisprudence" \
  --tags "Islamic Lecture; Fiqh; Urdu; Jurisprudence"

# Output:
# Upload Summary
# ===================================
# Identifier: 21-al-shurb-e-khamr-lecture-series
# Title:      21 Al Shurb e Khamr Lecture Series
# Creator:    Sheikh Mohammad Mohsin
# Collection: opensource_audio
# Tags:       Islamic Lecture; Fiqh; Urdu; Jurisprudence; Al Shurb e Khamr
# Files:      2 total, 2 to upload
#
# Uploading...
# [1/2] Uploading: thumbnail.jpg
#   ✓ Success
# [2/2] Uploading: Al-Shurb-e-Khamr_Dars 01.mp3
#   ✓ Success
#
# Upload complete!
# URL: https://archive.org/details/21-al-shurb-e-khamr-lecture-series
# Moved to: audio-uploaded-done/21_Al-Shurb-e-Khamr (02)
```

### Example 2: Dry-run Preview

```bash
python scripts/upload_to_archive.py audio_folders/22_Al-Murtad \
  --creator "Sheikh Mohammad Mohsin" \
  --description "Test" \
  --tags "test" \
  --dry-run

# Shows upload summary without uploading
# Files remain in audio_folders/
```

### Example 3: Resume Failed Upload

If upload is interrupted, simply run again:

```bash
python scripts/upload_to_archive.py audio_folders/21_Al-Shurb-e-Khamr \
  --creator "Sheikh Mohammad Mohsin" \
  --description "Description" \
  --tags "tags"

# Output:
# [RESUME] Found checkpoint: 5 files already uploaded
# [RESUME] Remaining files: 3
#
# Uploading...
# [6/8] Uploading: file6.mp3
#   ✓ Success
```

### Example 4: With Custom Collection

```bash
python scripts/upload_to_archive.py audio_folders/21_Al-Shurb-e-Khamr \
  --creator "Sheikh Mohammad Mohsin" \
  --description "Description" \
  --tags "tags" \
  --collection "islamic_lectures"
```

## Auto-Generated Metadata

### Title Format

```
{chapter_number} {Chapter Name} Lecture Series
```

**Examples:**
- `21 Al Shurb e Khamr Lecture Series`
- `12 Al Eela Lecture Series`
- `22 Al Murtad Lecture Series`

**Generation:**
- Chapter number extracted from folder name (e.g., "21_Al-Shurb...")
- Chapter name extracted and hyphens converted to spaces
- Lecture count removed from display

### Identifier Format

```
{chapter_number}-{chapter_name}-lecture-series
```

**Examples:**
- `21-al-shurb-e-khamr-lecture-series`
- `12-al-eela-lecture-series`

**Rules:**
- Lowercase only
- Hyphens between words
- No spaces or special characters
- Includes "lecture-series" suffix
- Archive.org URL: `https://archive.org/details/{identifier}`

### Description Template

```
{Chapter Name} - Islamic Fiqh lecture series by {Creator}.
Part of Al Fiqh ul Ahwat course.
Contains {N} lectures in Urdu.
```

**Example:**
```
Al Shurb e Khamr - Islamic Fiqh lecture series by Sheikh Mohammad Mohsin.
Part of Al Fiqh ul Ahwat course.
Contains 3 lectures in Urdu.
```

### Tags Generation

Auto-generated tags include:
- Chapter name keywords
- Base tags: "Islamic Lecture; Fiqh; Urdu"
- Speaker name (from creator)
- User-provided tags

**Example:**
```
Islamic Lecture; Fiqh; Urdu; Al Shurb e Khamr; Sheikh Mohammad Mohsin
```

## Identifier Rules

### Valid Format

- Lowercase letters: a-z ✓
- Numbers: 0-9 ✓
- Hyphens: - ✓

### Invalid Format

```
❌ Uppercase: 21-Al-Shurb  (will error)
❌ Spaces: 21 al shurb  (will error)
❌ Underscores: 21_al_shurb  (will error)
❌ Special chars: 21-al/shurb  (will error)
```

**Error Message:**
```
Error: Identifier must be lowercase letters, numbers, and hyphens only
```

## Checkpointing System

### How It Works

The script saves progress after each successful file upload:

```
.upload_checkpoints/
├── 21-al-shurb-e-khamr-lecture-series.json
├── 12-al-eela-lecture-series.json
└── 22-al-murtad-lecture-series.json
```

### Checkpoint File Structure

```json
{
  "uploaded_files": [
    "thumbnail.jpg",
    "Al-Shurb-e-Khamr_Dars 01.mp3",
    "Al-Shurb-e-Khamr_Dars 02.mp3"
  ],
  "failed_files": []
}
```

### Resume Behavior

On re-run with same identifier:
1. Loads checkpoint
2. Skips already-uploaded files
3. Resumes with remaining files
4. Updates checkpoint after each upload
5. Clears checkpoint on complete success

### Manual Checkpoint Management

**Delete checkpoint to restart upload:**
```bash
rm .upload_checkpoints/identifier.json
```

## Thumbnail/Cover Generation

### Auto-generation

If `Pillow` is installed, the script automatically:
1. Creates a thumbnail image
2. Adds speaker name and chapter info
3. Uploads thumbnail first
4. Archives use it as cover image

### Manual Thumbnail

Provide `thumbnail.jpg` in folder:
```
audio_folders/21_Al-Shurb-e-Khamr/
├── thumbnail.jpg  (optional, will use if present)
├── Al-Shurb-e-Khamr_Dars 01.mp3
├── Al-Shurb-e-Khamr_Dars 02.mp3
```

### Disable Thumbnail

Not currently configurable via CLI. Edit script if needed:
```python
generate_cover=False  # Change in main() if desired
```

## Folder Organization

### After Successful Upload

Folder is automatically moved:

```
BEFORE:
audio_folders/
├── 21_Al-Shurb-e-Khamr (02)/
│   ├── Al-Shurb-e-Khamr_Dars 01.mp3
│   └── Al-Shurb-e-Khamr_Dars 02.mp3

AFTER:
audio-uploaded-done/
├── 21_Al-Shurb-e-Khamr (02)/
│   ├── Al-Shurb-e-Khamr_Dars 01.mp3
│   └── Al-Shurb-e-Khamr_Dars 02.mp3
```

### Disable Auto-move

Edit `scripts/upload_to_archive.py`:
```python
upload_to_archive(..., auto_move=False)  # Keep folder in audio_folders/
```

## Supported Audio Formats

- `.mp3` - MPEG Audio (recommended)
- `.m4a` - iTunes/Apple Audio
- `.wav` - Uncompressed Audio
- `.flac` - Free Lossless Audio
- `.ogg` - Ogg Vorbis Audio

## Error Handling

### Authentication Error

```
Error: Invalid credentials. Run: ia configure
```

**Solution:**
```bash
ia configure  # Re-enter credentials
```

### Upload Fails

```
[2/5] Uploading: file.mp3
✗ Failed (status: [400])
[CHECKPOINT] Progress saved. Run again to resume from file 2.
```

**Solution:**
1. Check file size (archive.org has limits per file)
2. Check internet connection
3. Run same command again to resume
4. Check archive.org status: https://status.archive.org

### Item Already Exists

```
Error: Item already exists on archive.org
```

**Solution:**
1. Use different identifier: `--identifier "custom-name"`
2. Delete old item on archive.org (if you own it)

### Dry-run Mode

```bash
python scripts/upload_to_archive.py <folder> \
  --creator "Name" \
  --description "Desc" \
  --tags "tags" \
  --dry-run

# Shows upload summary without uploading
# Useful for testing identifiers and metadata
```

## Integration with Pipeline

This skill is **Step 3** in the audio processing pipeline:

```
Step 1: Rename files & folders (urdu-audio-renamer)
         ↓
Step 2: Edit metadata tags (audio-metadata-editor)
         ↓
Step 3: Upload to archive.org (this skill)
```

**Integrated pipeline command:**
```bash
python process_audio.py audio_folders/21_Chapter-Name
```

This automatically:
1. Renames files
2. Edits metadata
3. Uploads to archive.org
4. Moves folder to done

## Archive.org Collections

Common collections:

| Collection | Type | Use Case |
|-----------|------|----------|
| `opensource_audio` | General | Islamic lectures, educational content |
| `community_audio` | User-generated | Community-produced content |
| `my_collection` | Private | Personal/restricted access |

Request custom collection: https://archive.org/about/collection.php

## Limitations & Notes

- ✓ Supports files up to 5GB each
- ✓ Unlimited files per item
- ✗ Cannot delete files after upload (only archive.org admins can)
- ✗ Cannot rename items after creation
- ✓ Can add more files to existing item (via checkpoints)
- ✓ Metadata is searchable and indexed

## Troubleshooting

### "No audio files found"

```
No audio files found in {folder}
```

**Causes:**
- Folder is empty
- Files are in subdirectories
- Unsupported format

**Solution:** Check folder path and file extensions.

### Identifier Already Exists

**Problem:** Same identifier generated for different content.

**Solution:** Use `--identifier` to specify unique name:
```bash
python scripts/upload_to_archive.py folder \
  --identifier "unique-chapter-22" \
  --creator "Name" --description "Desc" --tags "tags"
```

### Slow Upload

**Causes:**
- Large files
- Slow internet connection
- Archive.org server load

**Solution:**
- Check internet speed: `speedtest-cli`
- Compress audio if possible
- Try again later if server slow

### Certificate/SSL Errors

```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Update certificates (macOS)
/Applications/Python\ 3.x/Install\ Certificates.command

# Or disable SSL verification (not recommended for production)
export PYTHONHTTPSVERIFY=0
python scripts/upload_to_archive.py ...
```

## API Reference

### Main Functions

```python
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
    """Upload folder to archive.org with checkpointing."""

def generate_title(folder: Path) -> str:
    """Generate title from folder name."""

def generate_identifier(folder: Path) -> str:
    """Generate archive.org identifier from folder name."""

def generate_description(folder: Path, creator: str) -> str:
    """Generate description from folder and creator."""

def generate_tags(folder: Path, base_tags: str = "...") -> str:
    """Generate tags from folder name and base tags."""

def load_checkpoint(identifier: str) -> dict:
    """Load checkpoint for resuming uploads."""

def save_checkpoint(identifier: str, checkpoint: dict):
    """Save upload progress checkpoint."""

def check_archive_exists(identifier: str) -> bool:
    """Check if item already exists on archive.org."""
```

## Performance

- **Upload speed:** Depends on file size and internet speed
- **Typical:** 50-200 MB/minute
- **Checkpointing:** ~100 KB metadata per upload

## References

- [Archive.org Metadata](https://archive.org/services/docs/api/metadata-schema/index.html) - Field reference
- [Internetarchive Library](https://internetarchive.readthedocs.io/) - Python library docs
- [Archive.org Collections](https://archive.org/collections/) - Available collections

## License

Part of the "Extract Your Human Job Into Skills" project.

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Verify archive.org credentials: `ia configure`
3. Try dry-run mode first: `--dry-run`
4. Check archive.org status: https://status.archive.org
5. Consult project documentation in `CLAUDE.md`
