#!/usr/bin/env python3
"""
Urdu Audio File Renamer
Renames Urdu audio files to Roman Urdu transliteration.

Usage:
    python rename_audio.py <folder_path> [--dry-run]
"""

import argparse
import io
import re
import sys
from pathlib import Path

# Fix Windows console encoding for Urdu text
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}

# Urdu to Roman transliteration map
TRANSLIT_MAP = {
    'ا': 'a', 'آ': 'aa', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ٹ': 't',
    'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd',
    'ڈ': 'd', 'ذ': 'z', 'ر': 'r', 'ڑ': 'r', 'ز': 'z', 'ژ': 'zh',
    'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z',
    'ع': '', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k', 'گ': 'g',
    'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'o', 'ہ': 'h', 'ھ': 'h',
    'ء': '', 'ی': 'i', 'ے': 'e', 'ئ': 'i', 'ؤ': 'o',
    # Common combined forms
    'ال': 'al',
}

# Words to strip from chapter names (not part of actual chapter name)
STRIP_WORDS = {'باب', 'کتاب', 'فصل'}

# Roman words to strip (for re-renaming incorrectly processed files)
STRIP_ROMAN = {'Bab', 'Kitab', 'Fasl'}

# Corrections for incorrectly transliterated Roman names
ROMAN_CORRECTIONS = {
    'Qsas': 'Qisas',
    'Tjart': 'Tijarat',
    'Qrz': 'Qarz',
}

# Common terms with preferred transliterations (standardized)
COMMON_TERMS = {
    # Basic terms (for reference, but باب is stripped)
    'درس': 'Dars',
    'حدیث': 'Hadees',
    'سورۃ': 'Surah',
    'آیت': 'Ayat',

    # Chapter names with ال (Arabic article) - already have Al-
    'الطہارت': 'Taharat',
    'الصلاۃ': 'Salat',
    'الصلوۃ': 'Salat',
    'الزکاۃ': 'Zakat',
    'الزکوۃ': 'Zakat',
    'الایلاء': 'Eela',
    'الظہار': 'Zihar',
    'اللعان': 'Laan',
    'العدۃ': 'Iddat',
    'الحج': 'Hajj',
    'الصوم': 'Saum',
    'البیوع': 'Buyoo',
    'البیع': 'Bay',
    'النکاح': 'Nikah',
    'الطلاق': 'Talaq',
    'الرضاع': 'Riza',
    'النفقات': 'Nafaqat',
    'الحدود': 'Hudood',
    'القضاء': 'Qaza',
    'الشہادات': 'Shahadat',
    'الوصیۃ': 'Wasiyyat',
    'الفرائض': 'Faraiz',
    'الوقف': 'Waqf',
    'الضمان': 'Zaman',

    # Chapter names without ال (Al- will be added automatically)
    'قصاص': 'Qisas',
    'تجارت': 'Tijarat',
    'حجر': 'Hajr',
    'صلح': 'Sulh',
    'عاریہ': 'Ariyat',
    'قرض': 'Qarz',
    'قرٖض': 'Qarz',
    'ودیعت': 'Wadiat',
    'شرب': 'Shurb',
    'خمر': 'Khamr',
    'مرتد': 'Murtad',
    'جہاد': 'Jihad',
    'غصب': 'Ghasab',
    'شفعہ': 'Shufah',
    'احیاء': 'Ahya',
    'موات': 'Mawat',
    'لقطہ': 'Luqta',
    'فرائض': 'Faraiz',
    'میراث': 'Miras',
    'وصیت': 'Wasiyyat',
    'نذر': 'Nazr',
    'قسم': 'Qasam',
    'کفارات': 'Kaffarat',
    'صید': 'Said',
    'ذبائح': 'Zabaih',
    'اطعمہ': 'Atima',
    'اشربہ': 'Ashriba',
    'لباس': 'Libas',
    'سکنی': 'Sukna',
    'اجارہ': 'Ijara',
    'وکالت': 'Wakalat',
    'اقرار': 'Iqrar',
    'ہبہ': 'Hiba',
    'سبق': 'Sabaq',
    'رمایہ': 'Rimaya',
}

# Sun letters for Arabic article assimilation
SUN_LETTERS = set('تثدذرزسشصضطظلن')


def transliterate_word(word: str) -> str:
    """Transliterate a single Urdu word to Roman."""
    # Check common terms first
    if word in COMMON_TERMS:
        return COMMON_TERMS[word]

    result = []
    i = 0
    while i < len(word):
        # Try two-character combinations first
        if i + 1 < len(word):
            two_char = word[i:i+2]
            if two_char in TRANSLIT_MAP:
                result.append(TRANSLIT_MAP[two_char])
                i += 2
                continue

        # Single character
        char = word[i]
        if char in TRANSLIT_MAP:
            result.append(TRANSLIT_MAP[char])
        elif char.isascii():
            result.append(char)
        # Skip diacritics and unknown characters
        i += 1

    transliterated = ''.join(result)
    # Capitalize first letter
    return transliterated.capitalize() if transliterated else ''


def is_roman_text(text: str) -> bool:
    """Check if text is already in Roman script (ASCII letters)."""
    return all(c.isascii() or c in '-_ ' for c in text)


def fix_roman_chapter_name(text: str) -> str:
    """Fix incorrectly processed Roman chapter names."""
    # Split by hyphen to get individual words
    parts = text.split('-')
    result = []

    for part in parts:
        # Skip Roman words that should be stripped
        if part in STRIP_ROMAN:
            continue
        # Apply corrections for misspelled names
        if part in ROMAN_CORRECTIONS:
            part = ROMAN_CORRECTIONS[part]
        if part:
            result.append(part)

    chapter_name = '-'.join(result)

    # Always add Al- prefix if not already present
    if chapter_name and not chapter_name.startswith('Al-'):
        chapter_name = 'Al-' + chapter_name

    return chapter_name


def transliterate_text(text: str) -> str:
    """Transliterate Urdu text to Roman, stripping باب/کتاب/فصل and adding Al- prefix."""
    # If text is already Roman (re-renaming case), fix it instead
    if is_roman_text(text):
        return fix_roman_chapter_name(text)

    words = text.split()
    result = []

    for word in words:
        # Skip words that should be stripped (باب، کتاب، فصل)
        if word in STRIP_WORDS:
            continue
        transliterated = transliterate_word(word)
        if transliterated:
            result.append(transliterated)

    chapter_name = '-'.join(result)

    # Always add Al- prefix if not already present
    if chapter_name and not chapter_name.startswith('Al-'):
        chapter_name = 'Al-' + chapter_name

    return chapter_name


def parse_filename(filename: str) -> tuple[str, int] | None:
    """
    Parse Urdu filename to extract chapter name and lesson number.
    Expected pattern: <Urdu Chapter Name> درس <number>
    Also handles already renamed files: <Roman-Name>_Dars-<number> or <Roman-Name>_Dars <number>
    Returns: (chapter_name, lesson_number) or None if parsing fails
    """
    # Pattern 1: Urdu text followed by درس and a number
    pattern_urdu = r'^(.+?)\s*درس\s*(\d+)$'
    match = re.match(pattern_urdu, filename, re.UNICODE)

    if match:
        chapter = match.group(1).strip()
        lesson_num = int(match.group(2))
        return (chapter, lesson_num)

    # Pattern 2: Already renamed Roman format (for re-renaming incorrectly processed files)
    # Matches: Bab-Qsas_Dars-01 or Al-Qisas_Dars 01
    pattern_roman = r'^(.+?)_Dars[- ](\d+)$'
    match = re.match(pattern_roman, filename)

    if match:
        chapter = match.group(1).strip()
        lesson_num = int(match.group(2))
        return (chapter, lesson_num)

    return None


def generate_new_filename(chapter: str, lesson_num: int, ext: str) -> str:
    """Generate new filename in standard format: Al-<Chapter-Name>_Dars <XX>.<ext>"""
    transliterated_chapter = transliterate_text(chapter)
    # Clean up any double hyphens
    transliterated_chapter = re.sub(r'-+', '-', transliterated_chapter)
    transliterated_chapter = transliterated_chapter.strip('-')

    return f"{transliterated_chapter}_Dars {lesson_num:02d}{ext}"


def get_safe_path(folder: Path, filename: str) -> Path:
    """Get a safe path, appending suffix if file exists."""
    target = folder / filename
    if not target.exists():
        return target

    stem = target.stem
    ext = target.suffix
    counter = 1

    while target.exists():
        target = folder / f"{stem}_{counter}{ext}"
        counter += 1

    return target


def parse_folder_name(folder_name: str) -> tuple[str, int] | None:
    """
    Parse folder name to extract chapter name and chapter number.
    Expected patterns:
    - Urdu: "باب قصاص 23" -> (قصاص, 23)
    - Roman: "23_Al-Qisas (17)" -> (Al-Qisas, 23)
    Returns: (chapter_name, chapter_number) or None if parsing fails
    """
    # Pattern 1: Urdu folder "باب <chapter> <number>"
    pattern_urdu = r'^(?:باب|کتاب|فصل)\s+(.+?)\s+(\d+)$'
    match = re.match(pattern_urdu, folder_name, re.UNICODE)
    if match:
        chapter = match.group(1).strip()
        chapter_num = int(match.group(2))
        return (chapter, chapter_num)

    # Pattern 2: Already renamed "<number>_<Chapter-Name> (<count>)"
    pattern_roman = r'^(\d+)_(.+?)\s*\(\d+\)$'
    match = re.match(pattern_roman, folder_name)
    if match:
        chapter_num = int(match.group(1))
        chapter = match.group(2).strip()
        return (chapter, chapter_num)

    return None


def generate_folder_name(chapter: str, chapter_num: int, file_count: int) -> str:
    """Generate new folder name: <Chapter-No>_Al-<Chapter-Name> (<Total-Lectures>)"""
    transliterated_chapter = transliterate_text(chapter)
    # Clean up any double hyphens
    transliterated_chapter = re.sub(r'-+', '-', transliterated_chapter)
    transliterated_chapter = transliterated_chapter.strip('-')

    return f"{chapter_num:02d}_{transliterated_chapter} ({file_count:02d})"


def process_folder(folder_path: str, dry_run: bool = False) -> list[tuple[str, str]]:
    """
    Process all audio files in folder and rename the folder itself.
    Returns list of (old_name, new_name) tuples.
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder_path}")

    results = []
    audio_files = []

    # First pass: collect audio files and count them
    for file_path in sorted(folder.iterdir()):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        if ext in AUDIO_EXTENSIONS:
            audio_files.append(file_path)

    file_count = len(audio_files)

    # Second pass: rename files
    for file_path in audio_files:
        ext = file_path.suffix.lower()
        stem = file_path.stem
        parsed = parse_filename(stem)

        if not parsed:
            print(f"  SKIP: {file_path.name} (could not parse)")
            continue

        chapter, lesson_num = parsed
        new_filename = generate_new_filename(chapter, lesson_num, ext)

        if new_filename == file_path.name:
            print(f"  SKIP: {file_path.name} (already renamed)")
            continue

        new_path = get_safe_path(folder, new_filename)

        results.append((file_path.name, new_path.name))

        if dry_run:
            print(f"  [DRY-RUN] {file_path.name} -> {new_path.name}")
        else:
            file_path.rename(new_path)
            print(f"  RENAMED: {file_path.name} -> {new_path.name}")

    # Rename folder
    folder_parsed = parse_folder_name(folder.name)
    if folder_parsed:
        chapter, chapter_num = folder_parsed
        new_folder_name = generate_folder_name(chapter, chapter_num, file_count)

        if new_folder_name != folder.name:
            new_folder_path = folder.parent / new_folder_name
            if dry_run:
                print(f"\n  [DRY-RUN] FOLDER: {folder.name} -> {new_folder_name}")
            else:
                if not new_folder_path.exists():
                    folder.rename(new_folder_path)
                    print(f"\n  FOLDER RENAMED: {folder.name} -> {new_folder_name}")
                else:
                    print(f"\n  FOLDER SKIP: {new_folder_name} already exists")
    else:
        print(f"\n  FOLDER SKIP: Could not parse folder name '{folder.name}'")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Rename Urdu audio files to Roman transliteration'
    )
    parser.add_argument('folder', help='Folder containing audio files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without renaming')

    args = parser.parse_args()

    print(f"Processing folder: {args.folder}")
    if args.dry_run:
        print("DRY-RUN MODE - No files will be renamed\n")

    try:
        results = process_folder(args.folder, args.dry_run)
        print(f"\nProcessed {len(results)} file(s)")
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
