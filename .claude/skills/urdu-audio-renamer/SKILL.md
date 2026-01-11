---
name: urdu-audio-renamer
description: Batch rename Urdu/Arabic audio files to Roman Urdu transliteration. Use when user wants to rename .mp3/.wav files with Urdu filenames, transliterate Islamic lecture recordings, or standardize audio file naming for courses with chapter names and lesson numbers (e.g., "باب الایلاء درس 1.mp3").
---

# Urdu Audio File Renamer

Rename audio files from Urdu to Roman Urdu using standard academic transliteration.

## Naming Conventions

### Files
```
Al-<Chapter-Name>_Dars <XX>.<ext>
```

### Folders
```
<Chapter-No>_Al-<Chapter-Name> (<Total-Lectures>)
```

## Al- Prefix Rule

- If original Urdu has "ال" (e.g., الایلاء) → transliterate as "Al-Eela"
- If original Urdu does NOT have "ال" (e.g., شرب خمر) → ADD "Al-" prefix → "Al-Shurb-e-Khamr"

All chapter names MUST start with "Al-" in the output.

## Examples

### Files
| Original | Renamed |
|----------|---------|
| باب الایلاء درس 1.mp3 | Al-Eela Dars 01.mp3 |
| باب شرب خمر درس 2.mp3 | Al-Shurb-e-Khamr Dars 02.mp3 |
| باب مرتد درس 3.mp3 | Al-Murtad Dars 03.mp3 |

### Folders
| Original | Renamed |
|----------|---------|
| باب الایلاء 12 | 12_Al-Eela (02) |
| باب شرب خمر 21 | 21_Al-Shurb-e-Khamr (02) |
| باب مرتد 22 | 22_Al-Murtad (03) |

## Usage

Run the rename script:

```bash
python scripts/rename_audio.py <folder_path> [--dry-run]
```

- `--dry-run`: Preview changes without renaming

## Transliteration

See [references/transliteration-map.md](references/transliteration-map.md) for character mappings and Arabic article assimilation rules.

## Constraints

- Rename in-place only; never modify audio content
- Prevent overwrites (append numeric suffix if conflict exists)
- Supported extensions: .mp3, .wav, .m4a, .flac, .ogg
