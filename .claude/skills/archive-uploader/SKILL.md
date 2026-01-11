---
name: archive-uploader
description: Upload audio files to archive.org with auto-generated metadata. Use when user wants to upload audio lectures, Islamic recordings, or any audio collection to Internet Archive. Claude generates description and tags from folder/file names. Triggers on requests to upload to archive.org, publish to Internet Archive, or batch upload audio files.
---

# Archive.org Uploader

Batch upload audio files to archive.org with auto-generated metadata.

## Scope

**Does:**
- Upload audio files to archive.org
- Auto-generate description and tags from folder/file names
- Create new archive.org items

**Does NOT:**
- Rename or modify local files
- Edit ID3 tags (use audio-metadata-editor skill)

## Prerequisites

1. **archive.org account** - Create at https://archive.org/account/signup
2. **Install library**: `pip install internetarchive`
3. **Configure credentials** (one-time):
   ```bash
   ia configure
   ```

## Required User Input

| Field | Required | Source |
|-------|----------|--------|
| `identifier` | Auto | `{chapter-name}-lecture-series` |
| `title` | Auto | `{chap_no}_{Chapter Name} Lecture Series` |
| `creator` | Yes | User provides (speaker name) |
| `description` | Auto | Claude generates from content |
| `subject/tags` | Auto | Claude generates from content |

## Auto-Generated Fields

**Title format:** `{chap_no}_{Chapter Name} Lecture Series`
- Example: `21_Al Shurb e Khamr Lecture Series`

**Identifier/URL format:** `{chapter-name}-lecture-series`
- Example: `al-shurb-e-khamr-lecture-series`
- URL: `https://archive.org/details/al-shurb-e-khamr-lecture-series`

**Description (Claude generates):**
```
{Chapter Name} - Islamic Fiqh lecture series by {Creator}.
Part of Al Fiqh ul Ahwat course. Contains {N} lectures in Urdu.
```

**Tags (Claude generates):**
- Chapter name keywords
- `Islamic Lecture`, `Fiqh`, `Urdu`
- Speaker name

## Processing Script

```bash
python scripts/upload_to_archive.py <folder> \
  --identifier "item-name" \
  --creator "Speaker Name" \
  --description "Auto-generated or custom" \
  --tags "tag1; tag2; tag3"
```

## Post-Upload Action

After successful upload, folder automatically moves:
```
audio_folders/{folder}  →  audio-uploaded-done/{folder}
```

## Workflow Integration

```
Skill 1: urdu-audio-renamer    → Rename files
Skill 2: audio-metadata-editor → Add ID3 tags
Skill 3: archive-uploader      → Upload to archive.org → Move to done folder
```
