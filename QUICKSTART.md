# Quick Start — File Index Project

**For any Claude session picking up this project**

---

## Starting a Session

**Use regular `cc` command** (no secrets required):

```bash
cd /path/to/file-index
cc  # or just 'claude' if cc not available
```

This project is **safe for restricted profiles** — only reads local files, no AWS secrets needed.

---

## Read These First (Order Matters)

1. **`README.md`** — Quick overview (2 min read)
2. **`CLAUDE.md`** — Full project context (5 min read)
3. **`PROGRESS.md`** — What's done, what's next (2 min read)
4. **`BUILD_PLAN.md`** — Development roadmap (reference)
5. **`TECH_STACK_RESEARCH.md`** — Why DuckDB? (reference)

---

## Current State

**Status:** Project initialized, ready to build Phase 1
**Next task:** Set up project structure and implement core indexer
**No blockers:** Ready to code

---

## What This Project Does

Solves: "Can't find files across projects"

Problems it fixes:
- Files are in unexpected directories
- Filenames don't match search terms
- No metadata search (tags, descriptions)
- grep/find are slow for large codebases

Solution: DuckDB index with tags, descriptions, and fast search (<100ms).

---

## How to Use (Simple)

**First time setup:**
```bash
# Copy example configs and customize
cp config/directories.yaml.example config/directories.yaml
cp config/tags.yaml.example config/tags.yaml
# Edit config/directories.yaml with your directory paths

# Install and build index
pip install -r requirements.txt
python -m src.indexer  # Build the index (20-30 seconds)
```

**Search (one command):**
```bash
python -m src.search "your search query"
python -m src.search --tag automation
python -m src.search --type script --category projects
python -m src.search --modified-after 2026-03-15
python -m src.search --stats  # Show index statistics
```

**Rebuild index (when files change):**
```bash
python -m src.indexer  # Re-indexes everything
```

## Development Commands

```bash
# Check status
git status
git log --oneline -5
cat PROGRESS.md

# Dry run (preview without writing)
python -m src.indexer --dry-run
```

---

## Phase 1 Tasks (Ready to Start)

See `BUILD_PLAN.md` for full details. High-level:

1. **M1: Setup** (30 min)
   - Create `requirements.txt`
   - Create `src/`, `config/`, `examples/` directories
   - Install dependencies

2. **M2: Schema** (30 min)
   - Create `src/schema.py`
   - Define DuckDB tables and indexes

3. **M3: Indexer** (2 hours)
   - Create `src/indexer.py`
   - Walk directories, extract metadata
   - Insert into DuckDB

4. **M4: Config** (30 min)
   - Create `config/directories.yaml`
   - Create `config/tags.yaml`

5. **M5: Search** (1 hour)
   - Create `src/search.py`
   - CLI tool with rich output

**Total Phase 1 time:** ~4-5 hours

---

## Technology Stack

- **DuckDB** — Blazing fast analytical database
- **Python 3.11+** — Already installed
- **watchdog** — File monitoring
- **rich** — Beautiful CLI output
- **PyYAML** — Config files

See `TECH_STACK_RESEARCH.md` for "why DuckDB vs SQLite vs JSON" comparison.

---

## Key Design Decisions

1. **Read-only** — Never modifies user files
2. **No secrets** — Only local file access
3. **Fast search** — <100ms for 100K files (target)
4. **Auto-updates** — Watches for file changes
5. **Rich metadata** — Tags, descriptions, relationships, commands

---

## Project Structure (Planned)

```
file-index/
├── 5-doc model             ✅ Complete
│   ├── CLAUDE.md
│   ├── BUILD_PLAN.md
│   ├── PROGRESS.md
│   ├── CHANGELOG.md
│   └── TECH_STACK_RESEARCH.md
├── README.md               ✅ Complete
├── .gitignore              ✅ Complete
├── requirements.txt        ⏳ To create
├── src/                    ⏳ To create
│   ├── __init__.py
│   ├── schema.py
│   ├── indexer.py
│   ├── search.py
│   └── watcher.py
├── config/                 ⏳ To create
│   ├── directories.yaml
│   └── tags.yaml
└── examples/               ⏳ To create
    └── search_examples.md
```

---

## Testing Strategy

**Phase 1 (MVP):**
1. Run `python -m src.indexer` to index configured directories
2. Search for files you know exist
3. Verify results match expectations
4. Check performance: search should complete in <100ms

**Success criteria:**
- Index builds successfully
- Search finds relevant files
- Fast results (<100ms)
- No sensitive data in index

---

## Common Questions

**Q: Why DuckDB instead of SQLite?**
A: DuckDB is optimized for analytical queries (filtering, searching). 10x faster for our use case. See `TECH_STACK_RESEARCH.md`.

**Q: How many files can it handle?**
A: Millions. DuckDB handles 100K+ files easily with sub-millisecond queries.

**Q: Does it modify my files?**
A: No. Read-only system. Only builds an index database.

**Q: What if the database gets corrupted?**
A: Delete `file_index.duckdb` and rebuild in <1 minute.

**Q: Can I version control the database?**
A: No, it's gitignored (too large, changes constantly). Rebuild from filesystem.

---

## Next Session Checklist

- [ ] Read `README.md`, `CLAUDE.md`, `PROGRESS.md`
- [ ] Check `git log` to see recent changes
- [ ] Review Phase 1 tasks in `BUILD_PLAN.md`
- [ ] Start with M1 (Setup) if ready to code
- [ ] Update `PROGRESS.md` as you complete tasks
- [ ] Commit frequently with clear messages
- [ ] Update `CHANGELOG.md` when milestones complete

---

## Git Workflow

```bash
# Start working
git status
git log --oneline -5

# Make changes
# (code, test, iterate)

# Commit
git add <files>
git commit -m "Implement feature

Details here.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Check what's done
git log --oneline -10
```

---

**Created:** 2026-03-20
**Last updated:** 2026-03-20
