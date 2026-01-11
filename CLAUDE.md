# Project: Extract Your Human Job Into Skills

This project automates the workflow for processing and uploading Islamic lecture audio files to archive.org.

## Quick Start (Recommended)

```bash
# Process single folder (tag + upload + move)
python process_audio.py audio_folders/21_Chapter-Name

# Process ALL pending folders
python process_audio.py --all

# Preview without changes
python process_audio.py --all --dry-run

# View upload history
python process_audio.py --history
```

## Skills Overview

| Skill | Purpose | Location |
|-------|---------|----------|
| **urdu-audio-renamer** | Rename Urdu audio files to Roman Urdu | `.claude/skills/urdu-audio-renamer/` |
| **audio-metadata-editor** | Edit ID3 metadata tags | `.claude/skills/audio-metadata-editor/` |
| **archive-uploader** | Upload to archive.org | `.claude/skills/archive-uploader/` |

## Complete Workflow

```
audio_folders/                    (input)
    ↓ Step 1: Tag metadata
    ↓ Step 2: Upload to archive.org
    ↓ Step 3: Move to done
audio-uploaded-done/              (completed)
```

## Project Structure

```
├── process_audio.py         # Unified pipeline (USE THIS)
├── config.yaml              # Default settings
├── upload_history.json      # Upload tracking (auto-generated)
├── CLAUDE.md                # This file
├── audio_folders/           # Pending folders
├── audio-uploaded-done/     # Completed uploads
└── .claude/skills/          # Individual skills
```

## Pipeline Commands

| Command | Description |
|---------|-------------|
| `python process_audio.py <folder>` | Process single folder |
| `python process_audio.py --all` | Process all pending |
| `python process_audio.py --tag-only` | Only add metadata |
| `python process_audio.py --upload-only` | Only upload |
| `python process_audio.py --dry-run` | Preview changes |
| `python process_audio.py --history` | View upload history |

## Features

- **Unified Pipeline**: Single command for entire workflow
- **Batch Processing**: `--all` processes all pending folders
- **Config File**: Edit `config.yaml` to change defaults
- **Upload History**: Tracks all uploads in `upload_history.json`
- **Duplicate Detection**: Skips already uploaded items
- **Auto-Move**: Moves folders to done after upload
- **Dry Run**: Preview changes before applying
- **Checkpointing**: Resume failed uploads from where they stopped
- **Thumbnail Generation**: Auto-creates cover images for archive.org

## Configuration (config.yaml)

```yaml
defaults:
  artist: "Sheikh Mohammad Mohsin"
  album: "Al Fiqh ul Ahwat Lecture Series"
  genre: "Islamic Jurisprudence"
  language: "Urdu"
  collection: "opensource_audio"
  base_tags: "Islamic Lecture; Fiqh; Urdu"

folders:
  input: "audio_folders"
  done: "audio-uploaded-done"
```

## Title/URL Format

- **Title:** `{chap_no} {Chapter Name} Lecture Series`
  - Example: `21 Al Shurb e Khamr Lecture Series`
- **Identifier:** `{chapter-name}-lecture-series`
  - Example: `al-shurb-e-khamr-lecture-series`

## Prerequisites

```bash
pip install mutagen internetarchive pyyaml pillow
ia configure  # One-time setup with API keys
```

## Individual Skill Commands (Legacy)

### Edit metadata only
```bash
python .claude/skills/audio-metadata-editor/scripts/edit_metadata.py <folder> --artist "Speaker Name"
```

### Upload only
```bash
python .claude/skills/archive-uploader/scripts/upload_to_archive.py <folder> \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "tag1; tag2"
```
