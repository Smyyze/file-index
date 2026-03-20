# File Index — Project Instructions

**Project type:** Coding project
**Status:** Planning / Initial setup
**Last updated:** 2026-03-20

---

## What This Project Does

Intelligent file indexing system using DuckDB for fast search across all your work files:
- Project directories
- Research outputs
- Documentation
- Any other directories you configure in `config/directories.yaml`

**Key features:**
- DuckDB database (fast analytical queries, millions of files)
- Full-text search (name, description, tags, content)
- Tag-based organization
- File relationships tracking
- Quick command lookup ("How do I upload to Google Docs?")
- Auto-updating (watches for file changes)

**Problem it solves:** Hard to find files when:
- They're in unexpected directories
- Filenames don't match search terms
- No central index of key files

With this system: `search "your query"` → instant results with path, tags, description

---

## Design Principles

1. **No secrets required** — Pure file scanning and indexing (safe for `cc` restricted profile)
2. **Fast > comprehensive** — Index key files, not every single file
3. **Maintainable** — Auto-update index when files change
4. **Simple queries** — CLI tool for quick lookups
5. **Extensible** — Easy to add new directories, tags, metadata

---

## 5-Doc Model

This project uses the proven 5-document structure from `C:\Users\cs\Projects\RESEARCH\ai_workflow_system`:

- **CLAUDE.md** (this file) — Project instructions, principles, context
- **BUILD_PLAN.md** — Development roadmap, milestones, tasks
- **PROGRESS.md** — Current status, what's done, what's next
- **CHANGELOG.md** — Record of changes with dates
- **TECH_STACK_RESEARCH.md** — Technology decisions and rationale

---

## Tech Stack (Already Decided)

- **Database:** DuckDB (fast analytical queries, single-file DB)
- **Language:** Python 3.11+
- **Dependencies:** duckdb, watchdog (file monitoring), rich (CLI formatting)
- **No secrets needed:** Reads local files only
- **Safe for:** `cc` restricted profile (no AWS Secrets Manager access)

---

## Project Structure

```
file-index/
├── CLAUDE.md              ← You are here
├── BUILD_PLAN.md          ← Development roadmap
├── PROGRESS.md            ← Current status
├── CHANGELOG.md           ← Change log
├── TECH_STACK_RESEARCH.md ← Technology decisions
├── src/
│   ├── indexer.py         ← Scans directories, builds index
│   ├── search.py          ← CLI search tool
│   ├── watcher.py         ← Auto-updates on file changes
│   └── schema.py          ← DuckDB schema definition
├── config/
│   ├── directories.yaml   ← Directories to index
│   └── tags.yaml          ← Tag definitions and rules
├── examples/
│   ├── search_examples.md ← Example queries
│   └── add_tags.md        ← How to add tags to files
├── file_index.duckdb      ← The database (gitignored)
└── README.md              ← Quick start guide
```

---

## Getting Started (For Claude Sessions)

**Read these first (in order):**
1. `BUILD_PLAN.md` — See the development roadmap
2. `PROGRESS.md` — See what's been done
3. `TECH_STACK_RESEARCH.md` — Understand the technology choices

**Current phase:** Phase 1 — Core indexing (not started yet)

**Quick commands:**
```bash
# Setup:
pip install -r requirements.txt

# Index files:
python -m src.indexer

# Search:
python -m src.search "your query"
python -m src.search --tag automation --type script
python -m src.search --stats
```

---

## Key Concepts

### Tags
Files are tagged automatically and manually:
- **Auto tags:** Derived from directory (`projects/`, `research/`), file type (`.py`, `.md`)
- **Manual tags:** Added via comments in files or separate tag file
- **Examples:** `upload`, `automation`, `google`, `healthcare`, `travel`, `taxes`

### Relationships
Files can be linked:
- Script → Documentation
- Example → Implementation
- Config → Code that uses it

### Quick Commands
Store executable commands with files:
- "Upload to Google Docs": `python scripts/upload_to_gdocs.py {file}`
- "Fill UHC claim": `python scripts/fill_uhc_interactive.py`

---

## Configuration

**Directories to index:**
Configure in `config/directories.yaml` with:
- Path to scan
- Category label (projects, research, etc.)
- Exclude patterns (git, caches, etc.)

**Auto-ignores:**
- `.git` directories
- `node_modules`, `venv`, `.venv`
- `__pycache__`, `.pytest_cache`
- Binary files (unless explicitly tagged)
- Sensitive folders (configure in `directories.yaml`)

---

## Use Cases

**Scenario 1: Find documentation**
```bash
$ python -m src.search "deployment setup"
Results: All files matching "deployment setup" in name/path/tags/description
```

**Scenario 2: Find all automation scripts**
```bash
$ python -m src.search --tag automation --type script
Results: All Python scripts tagged with automation
```

**Scenario 3: What changed this week?**
```bash
$ python -m src.search --modified-after 2026-03-17
Results: All files modified since March 17, 2026
```

---

## Safety & Security

**No secrets required:**
- Only reads local files
- No AWS, no external APIs
- Safe to run with `cc` restricted profile

**Respects privacy:**
- Excludes configured sensitive directories
- Doesn't index file contents by default (optional)
- Stores only metadata (path, tags, description)

**Doesn't change files:**
- Read-only operations
- Never modifies your files
- Only builds/updates the index database

---

## Future Enhancements (Post-MVP)

- [ ] Web UI (simple Flask app)
- [ ] File content indexing (optional, for full-text search in file bodies)
- [ ] AI-powered tag suggestions
- [ ] Integration with Claude Code (context awareness)
- [ ] Export/import index (share with team)
- [ ] Visual graph of file relationships

---

## Questions for Implementation

These will be answered in `BUILD_PLAN.md`:
- [ ] What directories to index first?
- [ ] How to handle large directories (>10K files)?
- [ ] Tag schema: free-form or predefined?
- [ ] CLI tool: rich/click/typer?
- [ ] How to add tags: comments in files? Separate YAML? Both?

---

**Created:** 2026-03-20
**Working directory:** `C:\Users\cs\Projects\file-index`
