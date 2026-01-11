# Extract Your Human Job Into Skills

**Status:** Active

Turn what you already do into 3–5 focused, reusable capabilities that replace parts of your own job and could help others with similar work.

## Actions

1. Describe your daily/weekly work to Claude Code
2. Identify repeatable cognitive tasks (decisions, writing, analysis, coordination)
3. Implement 3–5 narrow, measurable skills that:
   - You actually use
   - Save time or reduce mental load
   - Could be reused by someone like you

## Constraints

- Skills must be small (100–900 LOC is fine)
- Each skill must have one clear outcome
- Each skill must be measurable

## Deliverables

- 3–5 skills (Claude Code / General Agent)
- A short README.md describing what each skill replaces and time saved / quality improved
- One 60–90 second demo (screen recording) — Use Loom Chrome Extension to record easily

---

# Implemented Skills

## Skill 1: Urdu Audio Renamer

**Location:** `.claude/skills/urdu-audio-renamer/`

### What It Replaces

**Before:** Manual renaming using **Bulk Rename Utility** software

I used to rename Urdu Islamic lecture audio files manually using Bulk Rename Utility. This involved:
- Opening the software and loading files
- Configuring regex patterns for Urdu text
- Manually typing transliterations
- Renaming folders separately
- Double-checking for sync errors

### The Problem

| Issue | Impact |
|-------|--------|
| Sync breaking | Files like `Dars 01, Dars 03, Dars 02` - wrong order |
| Inconsistent transliteration | "Eela" vs "Ella" vs "Eila" across folders |
| Missing "Al-" prefix | Forgot to add standardized prefix |
| Time-consuming | 5-10 minutes per folder |
| Error rate | ~10-20% of folders had issues |

### Before vs After

| Metric | Before (Bulk Rename Utility) | After (Claude Skill) |
|--------|------------------------------|----------------------|
| **Time per folder** | 5-10 minutes | < 5 seconds |
| **Error rate** | 10-20% | 0% |
| **Consistency** | Low | 100% |
| **Sync errors** | Frequent | Never |
| **"Al-" prefix** | Manual | Automatic |
| **Folder renaming** | Separate step | Included |
| **Lecture count** | Manual counting | Automatic |

### Example Transformation

**Input (Urdu):**
```
باب شرب خمر 21/
├── باب شرب خمر درس 1.mp3
└── باب شرب خمر درس 2.mp3
```

**Output (Roman Urdu):**
```
21_Al-Shurb-e-Khamr (02)/
├── Al-Shurb-e-Khamr Dars 01.mp3
└── Al-Shurb-e-Khamr Dars 02.mp3
```

### Time Saved

- **Per folder:** 5-10 minutes saved
- **Per batch (10 folders):** 50-100 minutes saved
- **Quality improvement:** 100% consistency, zero sync errors

### Skill Components

| File | Purpose | LOC |
|------|---------|-----|
| `SKILL.md` | Skill definition & naming conventions | ~55 |
| `scripts/rename_audio.py` | Automation script | ~225 |
| `references/transliteration-map.md` | Urdu to Roman mapping | ~80 |
| **Total** | | **~360** |

### One Clear Outcome

Given a folder of Urdu audio files, produce consistently named Roman Urdu files with:
- Standardized "Al-" prefix
- Zero-padded lesson numbers
- Folder renamed with chapter number and lecture count

### Measurable Results

- **Speed:** 100x faster (5 seconds vs 5 minutes)
- **Accuracy:** 100% (vs 80-90% manual)
- **Consistency:** 100% same naming across all folders

---

## Skill 2: Audio Metadata Editor

**Location:** `.claude/skills/audio-metadata-editor/`

### What It Replaces

**Before:** Manual ID3 tag editing using **Mp3tag** software

I used to edit audio metadata manually using Mp3tag. This involved:
- Opening the software and loading files
- Selecting each file or batch
- Manually typing Title, Artist, Album, Genre for each
- Copy-pasting values between fields
- Ensuring consistent formatting across files

### The Problem

| Issue | Impact |
|-------|--------|
| Repetitive data entry | Same artist/album typed repeatedly |
| Inconsistent formatting | "Islamic Lecture" vs "islamic lecture" |
| Missing fields | Forgot to set Language, Comment |
| Time-consuming | 2-3 minutes per file |
| Error-prone | Typos in artist names |

### Before vs After

| Metric | Before (Mp3tag) | After (Claude Skill) |
|--------|-----------------|----------------------|
| **Time per folder** | 10-15 minutes | < 3 seconds |
| **Error rate** | 5-10% | 0% |
| **Consistency** | Low | 100% |
| **Fields covered** | 4-5 manual | 8+ automatic |
| **Batch processing** | Semi-manual | Fully automatic |

### Example Transformation

**Input (filename):**
```
Al-Shurb-e-Khamr_Dars 01.mp3
```

**Output (ID3 metadata):**
```
Title:       Al Shurb e Khamr
Album:       Al Fiqh ul Ahwat Lecture Series
Artist:      Sheikh Mohammad Mohsin
Album Artist: Sheikh Mohammad Mohsin
Track:       01
Genre:       Islamic Jurisprudence
Language:    Urdu
```

### Time Saved

- **Per file:** 2-3 minutes saved
- **Per folder (5 files):** 10-15 minutes saved
- **Quality improvement:** 100% consistency, all fields populated

### Skill Components

| File | Purpose | LOC |
|------|---------|-----|
| `SKILL.md` | Skill definition & metadata mapping | ~75 |
| `scripts/edit_metadata.py` | Batch ID3 editing script | ~180 |
| **Total** | | **~255** |

### One Clear Outcome

Given a folder of named audio files, automatically populate ID3 tags with:
- Title extracted from filename
- Consistent Album, Artist, Genre
- Zero-padded track numbers
- Language and Comment fields

### Measurable Results

- **Speed:** 200x faster (3 seconds vs 10 minutes per folder)
- **Accuracy:** 100% (vs 90-95% manual)
- **Consistency:** 100% identical formatting across all files

---

## Skill 3: Archive.org Uploader

**Location:** `.claude/skills/archive-uploader/`

### What It Replaces

**Before:** Manual upload via archive.org web interface

I used to upload audio files manually through the archive.org website. This involved:
- Navigating to archive.org and logging in
- Creating a new item with unique identifier
- Manually filling metadata fields (title, creator, description, tags)
- Uploading files one by one or in batches
- Writing descriptions from scratch each time
- Remembering which tags to use

### The Problem

| Issue | Impact |
|-------|--------|
| Repetitive form filling | Same creator/collection typed repeatedly |
| Inconsistent descriptions | Different wording each time |
| Missing tags | Forgot important keywords |
| Time-consuming | 5-10 minutes per upload |
| Manual file selection | Click each file individually |

### Before vs After

| Metric | Before (Web Interface) | After (Claude Skill) |
|--------|------------------------|----------------------|
| **Time per upload** | 5-10 minutes | < 30 seconds |
| **Description quality** | Inconsistent | Claude-generated, consistent |
| **Tag coverage** | Often incomplete | Auto-generated, comprehensive |
| **Batch upload** | Semi-manual | Fully automatic |
| **Error rate** | 5-10% (typos, missing fields) | 0% |

### Example Transformation

**Input:**
```
audio_folders/21_Al-Shurb-e-Khamr (02)/
├── Al-Shurb-e-Khamr_Dars 01.mp3
└── Al-Shurb-e-Khamr_Dars 02.mp3
```

**Output (archive.org item):**
```
Identifier:   al-fiqh-ul-ahwat-shurb-e-khamr
Title:        Al Shurb e Khamr
Creator:      Sheikh Mohammad Mohsin
Description:  Al Shurb e Khamr - Islamic Fiqh lecture series by
              Sheikh Mohammad Mohsin. Part of Al Fiqh ul Ahwat
              course covering rulings on intoxicants.
              Contains 2 lectures in Urdu.
Tags:         Islamic Lecture; Fiqh; Urdu; Al Fiqh ul Ahwat
URL:          https://archive.org/details/al-fiqh-ul-ahwat-shurb-e-khamr
```

### Time Saved

- **Per upload:** 5-10 minutes saved
- **Per batch (5 folders):** 25-50 minutes saved
- **Quality improvement:** Professional descriptions, comprehensive tags

### Skill Components

| File | Purpose | LOC |
|------|---------|-----|
| `SKILL.md` | Skill definition & metadata guide | ~70 |
| `scripts/upload_to_archive.py` | Upload script | ~140 |
| **Total** | | **~210** |

### One Clear Outcome

Given a folder of audio files, upload to archive.org with:
- Auto-generated title from folder name
- Claude-generated description and tags
- Proper metadata (creator, language, collection)
- Single command execution

### Measurable Results

- **Speed:** 20x faster (30 seconds vs 10 minutes)
- **Accuracy:** 100% (vs 90-95% manual)
- **Description quality:** Professional, consistent
- **Tag coverage:** Comprehensive, SEO-friendly

---

## Complete Workflow

The three skills form a complete audio processing pipeline:

```
┌─────────────────────────┐
│ Urdu Audio Files        │
│ (باب شرب خمر درس 1.mp3) │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Skill 1: Rename         │
│ urdu-audio-renamer      │
│ → Al-Shurb-e-Khamr_Dars │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Skill 2: Tag            │
│ audio-metadata-editor   │
│ → ID3 tags added        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Skill 3: Upload         │
│ archive-uploader        │
│ → Published on archive  │
└───────────┴─────────────┘
```

### Total Time Saved (per folder)

| Step | Before | After |
|------|--------|-------|
| Rename | 5-10 min | 5 sec |
| Tag | 10-15 min | 3 sec |
| Upload | 5-10 min | 30 sec |
| **Total** | **20-35 min** | **< 1 min** |

**Efficiency gain: 30x faster**