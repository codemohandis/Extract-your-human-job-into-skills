# Urdu Audio File Renamer

Batch rename Urdu/Arabic audio files to standardized Roman Urdu transliteration with proper chapter naming conventions.

## Overview

This skill automates the renaming of Islamic lecture audio files from Urdu script to Roman Urdu (Latin characters), following academic transliteration standards. It handles both individual file renaming and folder name standardization.

## Features

- **Automatic Urdu-to-Roman transliteration** using academic standards
- **Smart Arabic article handling** - adds "Al-" prefix where needed
- **Batch processing** - rename entire folders at once
- **Folder renaming** - standardizes folder names with chapter numbers
- **Re-renaming support** - detects and fixes already-processed files
- **Conflict prevention** - adds numeric suffix to avoid overwrites
- **Dry-run mode** - preview changes before applying
- **Multi-format support** - handles .mp3, .wav, .m4a, .flac, .ogg

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version
```

No external dependencies required. The script uses only Python standard library.

### Usage

#### Basic Usage

```bash
# Rename files and folder in a directory
python scripts/rename_audio.py <folder_path>

# Preview changes without renaming
python scripts/rename_audio.py <folder_path> --dry-run
```

#### Examples

**Example 1: Single folder processing**
```bash
python scripts/rename_audio.py audio_folders/21_Al-Shurb-e-Khamr

# Output:
# Processing folder: audio_folders/21_Al-Shurb-e-Khamr
# RENAMED: باب شرب خمر درس 1.mp3 -> Al-Shurb-e-Khamr_Dars 01.mp3
# RENAMED: باب شرب خمر درس 2.mp3 -> Al-Shurb-e-Khamr_Dars 02.mp3
# FOLDER RENAMED: باب شرب خمر 21 -> 21_Al-Shurb-e-Khamr (02)
```

**Example 2: Dry-run preview**
```bash
python scripts/rename_audio.py audio_folders/22_Chapter --dry-run

# Output shows what WOULD be renamed without making changes
```

## Naming Conventions

### File Format

```
Al-<Chapter-Name>_Dars <XX>.<ext>
```

**Examples:**
- `Al-Eela_Dars 01.mp3`
- `Al-Shurb-e-Khamr_Dars 02.mp3`
- `Al-Murtad_Dars 03.mp3`

### Folder Format

```
<Chapter-No>_Al-<Chapter-Name> (<Total-Lectures>)
```

**Examples:**
- `21_Al-Shurb-e-Khamr (02)`
- `12_Al-Eela (03)`
- `22_Al-Murtad (05)`

## Transliteration Rules

### Arabic Article (ال)

**Rule 1: Text WITH "ال" (Arabic article)**
- Original Urdu: `الایلاء` → Transliterated: `Eela` → Final: `Al-Eela`
- The "ال" is removed during transliteration, then "Al-" is automatically added

**Rule 2: Text WITHOUT "ال"**
- Original Urdu: `شرب خمر` → Transliterated: `Shurb Khamr` → Final: `Al-Shurb-e-Khamr`
- "Al-" prefix is automatically added if not present

**Result:** All chapter names must start with "Al-" in the output.

### Character Mapping

The script uses standard academic transliteration for Urdu/Arabic characters:

| Urdu | Roman | Urdu | Roman |
|------|-------|------|-------|
| ا | a | ش | sh |
| آ | aa | ص | s |
| ب | b | ض | z |
| پ | p | ط | t |
| ت | t | ظ | z |
| ج | j | ع | (silent) |
| چ | ch | غ | gh |
| ح | h | ف | f |
| خ | kh | ق | q |
| د | d | ک | k |
| ڈ | d | گ | g |
| ذ | z | ل | l |
| ر | r | م | m |
| ڑ | r | ن | n |
| ز | z | و | o |
| ژ | zh | ہ | h |
| س | s | ی | i |

See [references/transliteration-map.md](references/transliteration-map.md) for complete mappings.

## Common Terms Dictionary

The script includes a built-in dictionary of 50+ Islamic jurisprudence terms:

```
الایلاء → Al-Eela
الصلاۃ → Al-Salat
الحج → Al-Hajj
الصوم → Al-Saum
البیوع → Al-Buyoo
النکاح → Al-Nikah
الطلاق → Al-Talaq
الرضاع → Al-Riza
```

### Adding Custom Terms

Edit the `COMMON_TERMS` dictionary in `scripts/rename_audio.py`:

```python
COMMON_TERMS = {
    'آپ کا اردو': 'Your-Transliteration',
    ...
}
```

## Processing Details

### File Parsing

The script recognizes two filename patterns:

1. **Urdu pattern:** `<Urdu Text> درس <number>`
   - Example: `باب شرب خمر درس 1`

2. **Roman pattern:** `<Roman-Name>_Dars <number>` or `<Roman-Name>_Dars-<number>`
   - Example: `Al-Shurb-e-Khamr_Dars 01`

### Folder Parsing

The script recognizes two folder name patterns:

1. **Urdu pattern:** `باب <chapter> <number>` or `کتاب <chapter> <number>`
   - Example: `باب شرب خمر 21`

2. **Roman pattern:** `<number>_<Chapter-Name> (<count>)`
   - Example: `21_Al-Shurb-e-Khamr (02)`

### Conflict Resolution

If a target filename already exists, the script appends a numeric suffix:

```
Original:  Al-Eela_Dars 01_1.mp3  (if conflict found)
           Al-Eela_Dars 01_2.mp3  (if still conflicts)
```

## Integration with Pipeline

This skill is **Step 1** in the audio processing pipeline:

```
Step 1: Rename files & folders (this skill)
         ↓
Step 2: Edit metadata tags (audio-metadata-editor)
         ↓
Step 3: Upload to archive.org (archive-uploader)
```

**Pipeline command:**
```bash
python process_audio.py audio_folders/21_Chapter-Name
```

## Troubleshooting

### Files Not Renamed

**Problem:** "SKIP: filename (could not parse)"

**Solution:** Check filename format. Must contain درس (Dars) or _Dars pattern.

```
✓ Correct:  باب شرب خمر درس 1.mp3
✗ Wrong:    Chapter-Name-1.mp3
```

### Folder Not Renamed

**Problem:** "FOLDER SKIP: Could not parse folder name"

**Solution:** Folder must contain chapter number. Rename manually first:

```
✗ Before:   Islamic-Lectures
✓ After:    21_Al-Shurb-e-Khamr
```

### Already Renamed Files

**Problem:** "SKIP: filename (already renamed)"

**Solution:** The script detects files already in correct format. No action needed.

### Conflicts

**Problem:** "FOLDER SKIP: folder already exists"

**Solution:** Move or delete the existing folder, then retry.

## Advanced Features

### Re-renaming Support

If files were previously renamed incorrectly, the script will:
1. Detect the Roman format
2. Fix incorrect transliterations
3. Apply correct naming standard

Example:
```
Before: Qsas_Dars 01.mp3
After:  Al-Qisas_Dars 01.mp3  (QSS → Qisas correction)
```

### Character Fixes

The script automatically corrects common transliteration errors:

```python
ROMAN_CORRECTIONS = {
    'Qsas': 'Qisas',      # QSS → Qisas
    'Tjart': 'Tijarat',   # Commerce
    'Qrz': 'Qarz',        # Loan
}
```

## Supported Audio Formats

- `.mp3` - MPEG Audio
- `.wav` - WAV Audio
- `.m4a` - iTunes Audio
- `.flac` - Free Lossless Audio
- `.ogg` - Ogg Vorbis

## Output Structure

After processing:

```
audio_folders/
├── 21_Al-Shurb-e-Khamr (02)/
│   ├── Al-Shurb-e-Khamr_Dars 01.mp3
│   ├── Al-Shurb-e-Khamr_Dars 02.mp3
│   └── ... (more lectures)
├── 22_Al-Murtad (03)/
│   ├── Al-Murtad_Dars 01.mp3
│   ├── Al-Murtad_Dars 02.mp3
│   ├── Al-Murtad_Dars 03.mp3
│   └── ... (more lectures)
```

## Constraints & Guarantees

- ✓ Rename in-place only; never moves files to different directories
- ✓ Never modifies audio content - only filenames
- ✓ Prevents overwrites with numeric suffix
- ✓ UTF-8 safe for Urdu/Arabic characters
- ✓ Windows/Linux/Mac compatible
- ✗ Will NOT rename subdirectories (only processes files in specified folder)
- ✗ Will NOT create backup copies

## References

- [Transliteration Map](references/transliteration-map.md) - Complete character mappings
- [Islamic Jurisprudence Terms](references/transliteration-map.md#common-islamic-terms) - Dictionary of Fiqh terms

## API Reference

### Main Functions

```python
def transliterate_text(text: str) -> str:
    """Transliterate Urdu text to Roman with Al- prefix."""

def process_folder(folder_path: str, dry_run: bool = False) -> list[tuple[str, str]]:
    """Process all audio files and folder. Returns list of (old_name, new_name)."""

def parse_filename(filename: str) -> tuple[str, int] | None:
    """Parse filename to extract chapter name and lesson number."""

def parse_folder_name(folder_name: str) -> tuple[str, int] | None:
    """Parse folder name to extract chapter name and chapter number."""
```

## License

Part of the "Extract Your Human Job Into Skills" project.

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Review [references/transliteration-map.md](references/transliteration-map.md)
3. Consult project documentation in `CLAUDE.md`
