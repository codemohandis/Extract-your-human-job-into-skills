# Extract Your Human Job Into Skills

> **Automate Islamic lecture audio processing and uploading to archive.org in three simple steps.**

Convert Urdu audio files, add professional metadata, and publish to archive.org with a single command.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

---

## 🎯 Quick Start

```bash
# Process a single folder (rename → tag → upload → move)
python process_audio.py audio_folders/21_Chapter-Name

# Process ALL pending folders at once
python process_audio.py --all

# Preview changes without applying them
python process_audio.py --all --dry-run

# View all completed uploads
python process_audio.py --history
```

**That's it!** Your audio files are renamed, tagged, uploaded to archive.org, and organized automatically.

---

## 📺 Learn by Watching

**[▶ Watch the Tutorial](https://placeholder.video/tutorial)** *(Click to see the complete workflow in action)*

---

## ✨ What This Project Does

### 1️⃣ **Rename Urdu Audio Files** (`urdu-audio-renamer`)
   - Converts Urdu/Arabic filenames to standardized Roman Urdu
   - Adds chapter numbers and lesson identifiers
   - Example: `باب شرب خمر درس 1.mp3` → `21_Al-Shurb-e-Khamr_Dars 01.mp3`

### 2️⃣ **Edit Audio Metadata** (`audio-metadata-editor`)
   - Adds professional ID3 tags (title, artist, album, track number)
   - Prepares files for search and discovery
   - Works with all major audio formats

### 3️⃣ **Upload to archive.org** (`archive-uploader`)
   - Batch uploads to Internet Archive
   - Auto-generates thumbnails and descriptions
   - Resumable uploads (if interrupted, just re-run)
   - Automatic duplicate detection

---

## 🚀 Complete Workflow

```
┌─────────────────┐
│ audio_folders/  │  (Urdu audio files)
│   21_Chapter    │
│   22_Chapter    │
└────────┬────────┘
         │
         ▼
    [Step 1: RENAME]     (urdu-audio-renamer)
    Convert Urdu filenames to Roman Urdu
         │
         ▼
    [Step 2: TAG]        (audio-metadata-editor)
    Add ID3 metadata
         │
         ▼
    [Step 3: UPLOAD]     (archive-uploader)
    Upload to archive.org
         │
         ▼
┌──────────────────────┐
│ audio-uploaded-done/ │  (Completed uploads)
└──────────────────────┘
```

**All handled by one command:**
```bash
python process_audio.py --all
```

---

## 📦 Skills Overview

| Skill | Purpose | Learn More |
|-------|---------|-----------|
| 🔤 **urdu-audio-renamer** | Rename Urdu files to Roman Urdu with chapter formatting | [Read Docs](/.claude/skills/urdu-audio-renamer/) |
| 🏷️ **audio-metadata-editor** | Add professional ID3 tags (artist, album, title, etc.) | [Read Docs](/.claude/skills/audio-metadata-editor/) |
| 📤 **archive-uploader** | Upload to archive.org with auto-generated metadata | [Read Docs](/.claude/skills/archive-uploader/) |

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for archive.org uploads)

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd 01_Extract Your Human Job Into Skills

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install mutagen internetarchive pyyaml pillow
```

### Step 3: Configure Archive.org Credentials

Only needed once:

```bash
ia configure
```

You'll be prompted for:
- Email address
- API access key
- API secret key

[Get your API credentials →](https://archive.org/account/s3.php)

### Step 4: Verify Setup

```bash
ia list --help  # Should work without errors
```

---

## 📋 Pipeline Commands

| Command | Description |
|---------|-------------|
| `python process_audio.py <folder>` | Process single folder through entire pipeline |
| `python process_audio.py --all` | Process all pending folders |
| `python process_audio.py --all --dry-run` | Preview changes without applying |
| `python process_audio.py --tag-only <folder>` | Only rename and add metadata (skip upload) |
| `python process_audio.py --upload-only <folder>` | Only upload (assumes already tagged) |
| `python process_audio.py --history` | View all completed uploads |

---

## 🎬 Real-World Examples

### Example 1: Process a Single Chapter

```bash
python process_audio.py audio_folders/21_Al-Shurb-e-Khamr

# What happens:
# ✓ Renames files: باب شرب خمر درس 1 → Al-Shurb-e-Khamr_Dars 01
# ✓ Adds metadata: title, artist, album, track number
# ✓ Uploads to archive.org
# ✓ Moves to audio-uploaded-done/
# ✓ Result: https://archive.org/details/21-al-shurb-e-khamr-lecture-series
```

### Example 2: Batch Process All Folders

```bash
python process_audio.py --all

# Processes:
# audio_folders/21_Chapter-A
# audio_folders/22_Chapter-B
# audio_folders/23_Chapter-C
# ... (all folders in sequence)
```

### Example 3: Preview Before Processing

```bash
python process_audio.py --all --dry-run

# Shows what WOULD happen without making any changes
# Perfect for testing!
```

---

## ⚙️ Configuration (config.yaml)

Customize defaults:

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

---

## 📁 Project Structure

```
.
├── process_audio.py              # Main unified pipeline (USE THIS!)
├── config.yaml                   # Configuration file
├── upload_history.json           # Auto-generated upload log
├── README.md                     # This file
├── CLAUDE.md                     # Technical documentation
│
├── audio_folders/                # Input: Your audio files here
│   ├── 21_Chapter-Name/
│   ├── 22_Chapter-Name/
│   └── ...
│
├── audio-uploaded-done/          # Output: Completed uploads
│   ├── 21_Chapter-Name/
│   ├── 22_Chapter-Name/
│   └── ...
│
└── .claude/skills/               # Individual tools (legacy)
    ├── urdu-audio-renamer/
    ├── audio-metadata-editor/
    └── archive-uploader/
```

---

## ✨ Key Features

- ✅ **Unified Pipeline** - One command for the entire workflow
- ✅ **Batch Processing** - Handle 100+ folders automatically
- ✅ **Smart Metadata** - Auto-generates titles, descriptions, tags
- ✅ **Resumable Uploads** - Interrupted? Just re-run the command
- ✅ **Duplicate Detection** - Skip already-uploaded items
- ✅ **Dry-Run Mode** - Preview changes before applying
- ✅ **Auto-Organization** - Folders move to "done" after upload
- ✅ **Thumbnail Generation** - Auto-creates cover images
- ✅ **Upload History** - Track all uploads in `upload_history.json`
- ✅ **Cross-Platform** - Works on Windows, macOS, Linux

---

## 🔧 For Advanced Users

### Use Individual Skills (Legacy)

If you need more control, use skills individually:

```bash
# Step 1: Rename files
python .claude/skills/urdu-audio-renamer/scripts/rename_audio.py <folder>

# Step 2: Edit metadata
python .claude/skills/audio-metadata-editor/scripts/edit_metadata.py <folder> \
  --artist "Speaker Name"

# Step 3: Upload
python .claude/skills/archive-uploader/scripts/upload_to_archive.py <folder> \
  --creator "Speaker Name" \
  --description "Description" \
  --tags "tag1; tag2"
```

See individual skill documentation for more options:
- [Urdu Audio Renamer Docs](/.claude/skills/urdu-audio-renamer/README.md)
- [Audio Metadata Editor Docs](/.claude/skills/audio-metadata-editor/README.md)
- [Archive Uploader Docs](/.claude/skills/archive-uploader/README.md)

---

## ❓ Troubleshooting

### Files Not Renamed
**Problem:** "SKIP: filename (could not parse)"

**Solution:** Check filename format. Must follow pattern: `<Urdu Text> درس <number>`
```
✓ Correct:  باب شرب خمر درس 1.mp3
✗ Wrong:    Chapter-Name-1.mp3
```

### Upload Fails
**Problem:** "Failed (status: [400])"

**Solution:**
1. Check internet connection
2. Verify archive.org credentials: `ia configure`
3. Re-run command to resume from checkpoint
4. Check file sizes (archive.org has limits)

### No Files Found
**Problem:** "No audio files found in folder"

**Solution:**
1. Verify folder path is correct
2. Ensure audio files are directly in folder (not subfolders)
3. Check file extensions: .mp3, .wav, .m4a supported

### Metadata Not Showing
**Problem:** ID3 tags not visible in media player

**Solution:**
1. Close and reopen media player
2. Try different player (VLC, foobar2000)
3. Verify files were tagged: `python process_audio.py <folder> --dry-run`

**For more help:** See detailed troubleshooting in individual skill docs.

---

## 📊 Archive.org Integration

### What Gets Uploaded

Each upload creates an archive.org item with:

| Item | Format | Example |
|------|--------|---------|
| **Title** | `<Chapter#> <Chapter Name> Lecture Series` | `21 Al Shurb e Khamr Lecture Series` |
| **Identifier** | `<chapter#>-<name>-lecture-series` | `21-al-shurb-e-khamr-lecture-series` |
| **URL** | `https://archive.org/details/{identifier}` | [View Example](https://archive.org/details/21-al-shurb-e-khamr-lecture-series) |
| **Files** | All audio + thumbnail | MP3 files + cover image |
| **Metadata** | Searchable tags | Islamic Lecture, Fiqh, Urdu, etc. |

### View Your Uploads

After uploading, find them at:
```
https://archive.org/details/{identifier}
```

Example:
```
https://archive.org/details/21-al-shurb-e-khamr-lecture-series
```

---

## 🎓 Use Cases

- 📚 **Islamic Education** - Preserve and share lecture series
- 🎙️ **Podcast Distribution** - Upload lectures to archive.org
- 🔬 **Academic Content** - Organize scholarly materials
- 🌍 **Knowledge Sharing** - Make educational content freely available
- 🗂️ **Content Management** - Batch organize and upload audio

---

## 📝 Configuration Details

### Naming Conventions

**Files:**
```
<Chapter-Name>_Dars <XX>.<ext>
Example: Al-Eela_Dars 01.mp3
```

**Folders:**
```
<Chapter#>_<Chapter-Name> (<Total-Lectures>)
Example: 21_Al-Shurb-e-Khamr (02)
```

### Transliteration Rules

The script includes 50+ Islamic jurisprudence terms:

```
الایلاء → Al-Eela
الصلاۃ → Al-Salat
البیوع → Al-Buyoo
النکاح → Al-Nikah
```

[View complete transliteration map →](/.claude/skills/urdu-audio-renamer/references/transliteration-map.md)

---

## 🚀 Get Started Now

### Quickest Path (5 minutes)

1. **Install dependencies**
   ```bash
   pip install mutagen internetarchive pyyaml pillow
   ```

2. **Configure archive.org**
   ```bash
   ia configure
   ```

3. **Place your audio files**
   ```
   audio_folders/
   └── 21_Chapter-Name/
       ├── file1.mp3
       └── file2.mp3
   ```

4. **Run the pipeline**
   ```bash
   python process_audio.py audio_folders/21_Chapter-Name
   ```

5. **Check archive.org**
   ```
   https://archive.org/details/21-al-chapter-name-lecture-series
   ```

---

## 📖 Learn More

- **[Technical Documentation](CLAUDE.md)** - Advanced configuration and concepts
- **[Urdu Audio Renamer](/.claude/skills/urdu-audio-renamer/README.md)** - File renaming details
- **[Audio Metadata Editor](/.claude/skills/audio-metadata-editor/README.md)** - Metadata tagging guide
- **[Archive Uploader](/.claude/skills/archive-uploader/README.md)** - Upload and integration

---

## ❤️ Support & Feedback

- 🐛 **Report Issues** → [GitHub Issues](https://github.com/your-repo/issues)
- 💡 **Feature Requests** → [Discussions](https://github.com/your-repo/discussions)
- 📧 **Contact** → your-email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

**Built with:**
- Python 3.8+
- [Mutagen](https://mutagen.readthedocs.io/) - Audio metadata
- [Internet Archive API](https://internetarchive.readthedocs.io/) - Archive.org integration
- [Pillow](https://python-pillow.org/) - Image generation

---

## 🎬 Video Tutorial

### [▶ Watch Full Tutorial](https://placeholder.video/tutorial)

**In this video, you'll learn:**
- ✅ How to install and configure
- ✅ How to rename your first batch of files
- ✅ How to add professional metadata
- ✅ How to upload to archive.org
- ✅ How to handle errors and resume uploads

**Duration:** ~15 minutes | **Difficulty:** Beginner-Friendly

---

<div align="center">

### ⭐ If you find this useful, please [star the repository](https://github.com/your-repo) ⭐

### 🚀 [Get Started Now →](##-get-started-now)

---

**Extract Your Human Job Into Skills** © 2024 | Made with ❤️ for the Islamic education community

</div>
