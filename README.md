# File Index

**Intelligent file indexing and search system using DuckDB**

Find any file across your projects instantly with tags, descriptions, and relationships.

---

## Quick Start

**Index your files:**
```bash
cd /path/to/file-index

# First time: copy example configs
cp config/directories.yaml.example config/directories.yaml
cp config/tags.yaml.example config/tags.yaml
# Edit config/directories.yaml with your paths

pip install -r requirements.txt
python -m src.indexer
```

**Search (one command):**
```bash
python -m src.search "your search query"
python -m src.search --tag automation
python -m src.search --type script
```

**For new sessions:**
1. `QUICKSTART.md` — Start here
2. `CLAUDE.md` — Project instructions
3. `PROGRESS.md` — Current status

---

## The Problem

Hard to find files across projects because:
- Files are in unexpected locations
- Filenames don't match what you're looking for
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
$ python -m src.search "deployment"
Results: all files matching "deployment" in name, path, description, or tags

# Find by tags
$ python -m src.search --tag automation --type script
Results: all Python scripts tagged with automation

# Recent files
$ python -m src.search --modified-after 2026-03-15
Results: all files modified since March 15, 2026

# Combine filters
$ python -m src.search --category projects --type doc
Results: all documentation files in projects category
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
