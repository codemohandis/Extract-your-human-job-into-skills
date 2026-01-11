# Video Script: Extract Your Human Job Into Skills
## Islamic Lecture Audio Processing Automation

**Total Duration:** 60 seconds (expandable to 90 seconds)

---

## Scene 1: Problem Statement (0-5 seconds)
**Visual:** Show folder of Urdu-named audio files with timestamps/clocks
**Speaker:**
> "Uploading Islamic lecture audio to archive.org used to take hours. Renaming files in Urdu script, tagging metadata, creating thumbnails, uploading... it's repetitive work."

---

## Scene 2: The Solution Intro (5-10 seconds)
**Visual:** Animated transition showing "Extract Your Human Job Into Skills" title
**Speaker:**
> "Meet a project that automates the entire workflow with three specialized AI skills. One command does what used to take hours."

---

## Scene 3: Skill 1 - Urdu Audio Renamer (10-20 seconds)
**Visual:** CLI demo showing file renaming in real-time
```
RENAMED: باب شرب خمر درس 1.mp3 → Al-Shurb-e-Khamr_Dars 01.mp3
RENAMED: باب شرب خمر درس 2.mp3 → Al-Shurb-e-Khamr_Dars 02.mp3
FOLDER RENAMED: 21_Al-Shurb-e-Khamr (02)
```

**Speaker:**
> "Skill One: Urdu Audio Renamer. Automatically converts Urdu and Arabic filenames to standardized Roman Urdu transliteration. Batch processes entire folders with academic accuracy."

---

## Scene 4: Skill 2 - Audio Metadata Editor (20-30 seconds)
**Visual:** ID3 tag visualization showing metadata being applied to files
```
[EDIT] Al-Shurb-e-Khamr_Dars 01.mp3
  ✓ Title: Al Shurb e Khamr - Dars 01
  ✓ Artist: Sheikh Mohammad Mohsin
  ✓ Album: Al Fiqh ul Ahwat Lecture Series
  ✓ Genre: Islamic Jurisprudence
```

**Speaker:**
> "Skill Two: Audio Metadata Editor. Adds professional ID3 tags to every file. Title, artist, album, genre—all automatically extracted from filenames and applied in seconds."

---

## Scene 5: Skill 3 - Archive Uploader (30-45 seconds)
**Visual:** Upload progress bar and archive.org interface
```
[1/3] Uploading: thumbnail.jpg          ✓ Success
[2/3] Uploading: Al-Shurb-e-Khamr_Dars 01.mp3  ✓ Success
[3/3] Uploading: Al-Shurb-e-Khamr_Dars 02.mp3  ✓ Success

URL: https://archive.org/details/21-al-shurb-e-khamr-lecture-series
```

**Speaker:**
> "Skill Three: Archive Uploader. Uploads to archive.org with intelligent checkpointing—resume if interrupted. Auto-generates titles, descriptions, and tags. Creates cover art automatically. Even moves finished folders to a done directory."

---

## Scene 6: The Unified Pipeline (45-55 seconds)
**Visual:** Simple workflow diagram with one command
```bash
$ python process_audio.py audio_folders/21_Al-Shurb-e-Khamr
```

**Arrow flowing through three steps:**
```
Rename Files → Tag Metadata → Upload to Archive
    ✓             ✓              ✓
```

**Speaker:**
> "All three skills work together in one pipeline. A single command: rename, tag metadata, and upload. What took hours now takes minutes. Plus checkpointing means even interrupted uploads resume perfectly."

---

## Scene 7: Results & CTA (55-60 seconds)
**Visual:** Split screen showing before/after: messy folder → organized archive.org collection
**Speaker:**
> "Upload Islamic lectures efficiently. Preserve knowledge. Scale your content. All three skills are available now. Extract your human job into skills today."

**Visual:** Display links and GitHub repo

---

## Extended Version: 90 Seconds (Additional 30 seconds)

### Additional Content (60-90 seconds)

**Scene A: Feature Highlights (60-70 seconds)**
**Visual:** Bullet point animations
- Dry-run mode (preview before changes)
- Duplicate detection (never re-upload)
- Custom metadata configuration
- Cross-platform (Windows/Linux/Mac)
- UTF-8 safe for Urdu/Arabic

**Speaker:**
> "Special features: dry-run mode to preview everything first. Smart duplicate detection prevents re-uploading. Fully configurable for any speaker or collection. Works everywhere: Windows, Linux, or Mac."

**Scene B: Real-World Impact (70-80 seconds)**
**Visual:** Show multiple lecture series being processed, statistics
**Speaker:**
> "This isn't just faster—it's smarter. Every lecture is properly tagged, discoverable, and preserved. Perfect for Islamic scholars, educators, and knowledge preservation organizations."

**Scene C: Final CTA (80-90 seconds)**
**Visual:** GitHub logo, project folder structure animation
**Speaker:**
> "Ready to transform your workflow? Check the GitHub repository. Documentation covers everything from installation to advanced features. Join creators automating their content pipeline."

---

## Technical Notes

### Equipment Needed
- Terminal/CLI screen recording
- Archive.org account for demo
- Sample Urdu-named audio files (or use screenshot mockups)

### Recommended Tools
- ScreenFlow (Mac) / OBS (cross-platform)
- Audacity for voiceover
- Final Cut Pro / DaVinci Resolve for editing

### Demo Environment
```bash
# Setup demo
pip install mutagen internetarchive pyyaml pillow
ia configure  # Set up archive.org credentials
```

### Key Metrics to Highlight
- **Before:** 2-3 hours per upload (manual process)
- **After:** 5-10 minutes (automated pipeline)
- **Scalability:** Process 100+ lectures without additional effort
- **Accuracy:** 100% consistent metadata application

---

## Key Talking Points
1. **Automation Value:** "What took hours now takes minutes"
2. **Quality:** "Professional-grade metadata automatically"
3. **Reliability:** "Checkpointing means no lost progress"
4. **Accessibility:** "Works with Urdu, Arabic, and any language"
5. **Preservation:** "Preserve knowledge at scale"

---

## Hashtags & Social Media
```
#IslamicEducation #AudioPreservation #Automation #ArchiveOrg #Python #AI #Knowledge #Workflow
```

---

## Call-to-Action Links
- 📦 **GitHub Repository:** [Project Link]
- 📚 **Documentation:** `CLAUDE.md` in repository
- 🎓 **Skills Overview:** `.claude/skills/` directory
- 🔧 **Quick Start:** `python process_audio.py --help`

---

## Notes for Presenter
- Speak clearly but conversationally
- Pause at transition points for visual changes
- Emphasize time savings (the key value prop)
- Show real files/real uploads when possible
- Keep energy up—this is exciting automation!
- End with clear next steps for viewers
