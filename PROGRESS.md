# Progress — File Index

**Last updated:** 2026-03-20

---

## Current Status

**Phase:** Phase 1 complete (core indexing)
**Current task:** None — ready for Phase 2 (content indexing / smarter search)
**Next action:** Add content indexing (first N lines of text files) so search finds files by what's *in* them, not just filename/tags

---

## What's Done

- [x] Project created with 5-doc model
- [x] `CLAUDE.md` — project instructions and context
- [x] `BUILD_PLAN.md` — 5-phase development plan
- [x] `PROGRESS.md` — this file
- [x] `CHANGELOG.md` — change log
- [x] `TECH_STACK_RESEARCH.md` — DuckDB rationale
- [x] `requirements.txt` — duckdb, watchdog, rich, pyyaml
- [x] `src/schema.py` — DuckDB table + indexes
- [x] `src/indexer.py` — directory scanner, auto-tagging, inline tag extraction, dry-run, stats
- [x] `src/search.py` — CLI search by text / tag / type / category / date
- [x] `config/directories.yaml` — L-C and Projects directories configured
- [x] `config/tags.yaml` — extension + directory auto-tag rules
- [x] Verified: dry-run indexes 2,013 files in ~3 seconds

---

## What's Next

**Phase 2 — content indexing:**
1. Add `--content` flag to indexer: read first 100 lines of each text file into a `content` column
2. Include `content` in search query (ILIKE match)
3. This enables finding `GDOCS-UPLOAD-SETUP.md` via `"google docs"` even without tags

**Phase 3 — auto-update watcher:**
- `src/watcher.py` using `watchdog` to monitor directories and re-index on change

---

## Blockers

None. Project is functional for metadata search. Content search is the main gap.

---

## Known Limitations

- Search only matches filename, path, tags, and description — not file contents
- Most files only have auto-derived tags (extension + directory)
- Manual tags require `# tags: ...` comment or YAML frontmatter in the file

---

## Key Decisions Made

- **DuckDB over SQLite** — faster analytical queries
- **No content indexing in Phase 1** — keep it fast, add optionally later
- **YAML config** — human-readable, easy to add/remove directories
- **Read-only** — never modifies user files
- **No secrets** — safe for `cc` restricted profile

---

**Created:** 2026-03-20
