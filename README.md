# File Index

**Intelligent file indexing and search system using DuckDB**

Find any file across your projects instantly with tags, descriptions, and relationships.

---

## Quick Start

**Read first:**
1. `CLAUDE.md` — Project instructions and context
2. `PROGRESS.md` — Current status
3. `BUILD_PLAN.md` — Development roadmap

**For developers:**
```bash
cd C:/Users/cs/Projects/file-index
pip install -r requirements.txt

# Index directories (when ready)
python -m src.indexer --config config/directories.yaml

# Search
python -m src.search "google docs upload"
```

---

## The Problem

Today couldn't find `scripts/GDOCS-UPLOAD-SETUP.md` when searching for "google docs upload" because:
- It's in `scripts/` not `docs/` (unexpected location)
- Filename doesn't contain "google" (non-obvious name)
- No way to search by description or tags
- grep/find are slow and don't search metadata

---

## The Solution

Build a DuckDB-based file index with:
- ✅ **Fast search** (<100ms for 100K+ files)
- ✅ **Rich metadata** (tags, descriptions, quick commands)
- ✅ **Auto-updates** (watches for file changes)
- ✅ **File relationships** (related files linked)
- ✅ **No secrets** (safe for `cc` restricted profile)
- ✅ **Read-only** (never modifies your files)

---

## Example Usage

```bash
# Find files by name or description
$ search "google docs upload"
Results:
1. scripts/GDOCS-UPLOAD-SETUP.md
   Tags: [upload, google, docs, setup]
   Command: python scripts/upload_to_gdocs.py {file}

# Find by tags
$ search --tag automation --type script
Results:
1. scripts/fill_uhc_interactive.py - UHC claims automation
2. scripts/upload_to_gdocs.py - Google Docs upload
3. scripts/flight_search.py - Flight search

# Recent files
$ search --modified-after "7 days ago"
(All files modified in last 7 days)

# With related files
$ search "upload_to_gdocs.py" --related
Results:
1. scripts/upload_to_gdocs.py
   Related:
   - scripts/GDOCS-UPLOAD-SETUP.md (documentation)
   - scripts/upload_html_to_gdocs.py (variant)
```

---

## Technology

- **DuckDB** — Fast analytical database, perfect for searching
- **Python 3.11+** — Core implementation
- **watchdog** — File monitoring for auto-updates
- **rich** — Beautiful CLI output
- **YAML** — Human-readable configuration

See `TECH_STACK_RESEARCH.md` for rationale and comparisons.

---

## Project Structure

```
file-index/
├── CLAUDE.md              ← Project instructions
├── BUILD_PLAN.md          ← Development roadmap
├── PROGRESS.md            ← Current status
├── CHANGELOG.md           ← Change history
├── TECH_STACK_RESEARCH.md ← Technology decisions
├── README.md              ← This file
├── src/                   ← Source code (to be created)
├── config/                ← Configuration files
├── examples/              ← Usage examples
└── file_index.duckdb      ← The database (gitignored)
```

---

## Status

**Current:** Project initialized, ready to build
**Next:** Phase 1 — Core indexing
**Estimated:** 1-2 coding sessions to MVP

See `PROGRESS.md` for details.

---

## 5-Document Model

This project uses the proven structure from `C:\Users\cs\Projects\RESEARCH\ai_workflow_system`:

- **CLAUDE.md** — Instructions for AI agents
- **BUILD_PLAN.md** — Milestones and tasks
- **PROGRESS.md** — What's done, what's next
- **CHANGELOG.md** — Record of changes
- **TECH_STACK_RESEARCH.md** — Technology rationale

---

## Use Cases

1. **Find setup guides** — "google docs upload" → GDOCS-UPLOAD-SETUP.md
2. **Find automation scripts** — `--tag automation --type script`
3. **Find recent changes** — `--modified-after "last week"`
4. **Get quick commands** — Shows how to run scripts
5. **Discover related files** — Find docs for a script

---

## Safety

- **No secrets required** — Only reads local files
- **Read-only** — Never modifies your files
- **Privacy-respecting** — Excludes configured sensitive directories
- **Safe for `cc`** — Works with restricted AWS profile

---

**Created:** 2026-03-20
**Working directory:** `C:\Users\cs\Projects\file-index`
