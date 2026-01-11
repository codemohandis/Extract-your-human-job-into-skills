---
name: audio-metadata-editor
description: Batch edit ID3 metadata tags for lecture audio files intended for archive.org. Use when user wants to add/update metadata (title, artist, album, track number, genre) to MP3 files, especially Islamic lecture recordings with chapter-based naming like "Chapter-Name_Lecture-XX.mp3". Triggers on requests to tag audio files, set ID3 tags, prepare audio for archive.org, or batch-edit audio metadata.
---

# Audio Metadata Editor

Batch edit ID3 tags for lecture audio files.

## Scope

**Does:**
- Edit embedded ID3 metadata tags in audio files
- Process files in batch from a folder

**Does NOT:**
- Rename files or folders
- Upload to archive.org
- Modify audio content

## Input Requirements

- Folder containing audio files (.mp3)
- Files follow naming pattern: `<Chapter-Name>_Dars <XX>.<ext>`
- Example: `Al-Zaman_Dars 01.mp3`

**Filename Regex:**
```
^(?P<chapter>.+?)_Dars\s+(?P<num>\d+)\.(?P<ext>mp3|m4a|wav)$
```

## Required User Input

Before processing, collect:
1. **Speaker name** (Artist/Album Artist)
2. **Copyright/License** (optional, defaults to empty)
3. **Year** (optional)

## Metadata Mapping

| Field | Value |
|-------|-------|
| Title | `{Chapter Name}` |
| Track | `{XX}` (zero-padded) |
| Artist | Speaker name |
| Album | `Al Fiqh ul Ahwat Lecture Series` |
| Album Artist | Speaker name |
| Genre | `Islamic Jurisprudence` |
| Language | `Urdu` |
| Year | User-provided or empty |
| Comment | `{Chapter Name}` |
| Copyright | User-provided or empty |

## Processing Script

Run `scripts/edit_metadata.py`:

```bash
python scripts/edit_metadata.py <folder> --artist "Speaker Name" [--year 2024] [--copyright "License"]
```

## Error Handling

- **File doesn't match pattern**: Skip with warning, continue processing
- **Missing mutagen**: Install with `pip install mutagen`
- **Write error**: Log error, continue with next file

## Formatting Rules

- UTF-8 encoding for all text
- Track numbers zero-padded to 2 digits
- Hyphens in chapter names converted to spaces for display
- Roman Urdu / English only (no Urdu script)
