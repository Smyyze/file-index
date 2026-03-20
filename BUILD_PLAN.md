# Build Plan — File Index

**Last updated:** 2026-03-20
**Status:** Planning complete, ready to build Phase 1

---

## Phase 1 — Core Indexing (Week 1)

**Done when:** Can scan directories, build DuckDB index, and search files by name/tags.

### Setup (M1)
- [ ] `requirements.txt`: duckdb, watchdog, rich, pyyaml
- [ ] Project structure: `src/`, `config/`, `examples/`
- [ ] `.gitignore`: `file_index.duckdb`, `*.pyc`, `__pycache__/`

### Database Schema (M2)
- [ ] `src/schema.py` — DuckDB table definitions
  ```sql
  CREATE TABLE file_index (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      path TEXT NOT NULL UNIQUE,
      type TEXT,  -- 'script', 'doc', 'config', 'data'
      category TEXT,  -- 'project', 'research', 'automation', 'reference'
      tags TEXT[],  -- Array of tags
      description TEXT,
      quick_command TEXT,
      related_files TEXT[],
      created TIMESTAMP,
      modified TIMESTAMP,
      size_kb INTEGER
  );

  -- Full-text search index
  CREATE INDEX idx_fts ON file_index USING FTS(name, description, tags);

  -- Common queries
  CREATE INDEX idx_tags ON file_index((unnest(tags)));
  CREATE INDEX idx_modified ON file_index(modified);
  CREATE INDEX idx_type ON file_index(type);
  ```

### Core Indexer (M3)
- [ ] `src/indexer.py` — Main indexing engine
  - Reads `config/directories.yaml` for directories to scan
  - Recursively walks directories
  - Extracts metadata (size, dates, type)
  - Auto-tags based on directory/extension
  - Reads manual tags from file comments (optional)
  - Inserts/updates records in DuckDB
  - Progress bar (rich)
  - Dry-run mode (`--dry-run`)

### Configuration (M4)
- [ ] `config/directories.yaml` — Directories to index
  ```yaml
  directories:
    - path: C:/Users/cs/L-C
      category: life-ops
      exclude:
        - "**/.git/**"
        - "**/__pycache__/**"
        - "**/node_modules/**"

    - path: C:/Users/cs/Projects
      category: projects
      exclude:
        - "**/.git/**"
        - "**/venv/**"
        - "**/.venv/**"

    - path: C:/Users/cs/Projects/RESEARCH
      category: research
  ```

- [ ] `config/tags.yaml` — Tag rules
  ```yaml
  auto_tags:
    extensions:
      ".py": [script, python]
      ".md": [doc, markdown]
      ".yaml": [config]
      ".json": [config, data]

    directories:
      scripts: [script, automation]
      docs: [documentation]
      examples: [example, reference]

  tag_aliases:
    gdocs: [google-docs, google, docs, upload]
    automation: [automate, bot, script]
  ```

### Basic Search (M5)
- [ ] `src/search.py` — CLI search tool
  - `python -m src.search "query"` — Text search
  - `python -m src.search --tag automation` — Filter by tag
  - `python -m src.search --type script` — Filter by type
  - `python -m src.search --category projects` — Filter by category
  - `python -m src.search --modified-after 2026-03-01` — Date range
  - Rich table output with colors
  - Show: name, path, tags, description, quick_command

### Testing
- [ ] Manual test: Index `C:/Users/cs/L-C/scripts/`
- [ ] Verify: Find `GDOCS-UPLOAD-SETUP.md` with query "google docs"
- [ ] Verify: Find all `.py` scripts with `--type script`
- [ ] Verify: Search works in <100ms for 1000+ files

---

## Phase 2 — Smart Tagging (Week 2)

**Done when:** Files have rich, accurate tags from multiple sources.

### Tag Extraction (M6)
- [ ] Read tags from file comments:
  ```python
  # tags: upload, google, automation
  # description: Upload markdown to Google Docs
  ```

- [ ] Read tags from YAML frontmatter:
  ```markdown
  ---
  tags: [upload, google, automation]
  description: Upload markdown to Google Docs
  ---
  ```

- [ ] Manual tag file: `tags.yaml` in each directory

### Tag Management (M7)
- [ ] `python -m src.tag add {path} {tag}` — Add tag
- [ ] `python -m src.tag remove {path} {tag}` — Remove tag
- [ ] `python -m src.tag list {path}` — Show tags
- [ ] `python -m src.tag suggest {path}` — Suggest tags (based on filename, directory, content)

### Relationships (M8)
- [ ] Link related files:
  - Script → Documentation
  - Example → Implementation
  - Test → Code
- [ ] `python -m src.link add {file1} {file2}` — Link files
- [ ] Show related files in search results

---

## Phase 3 — Auto-Update (Week 3)

**Done when:** Index updates automatically when files change.

### File Watcher (M9)
- [ ] `src/watcher.py` — Monitor directories for changes
  - Uses `watchdog` library
  - Watches all configured directories
  - Detects: create, modify, delete, move
  - Updates index in real-time
  - Debounces (wait 1 sec before indexing)
  - Runs as background process

### Update Commands (M10)
- [ ] `python -m src.indexer --update` — Re-scan all files
- [ ] `python -m src.indexer --file {path}` — Re-index one file
- [ ] `python -m src.watcher --daemon` — Start background watcher

### Performance (M11)
- [ ] Incremental updates (only changed files)
- [ ] Batch updates (group multiple changes)
- [ ] Index statistics: `python -m src.stats`

---

## Phase 4 — Advanced Search (Week 4)

**Done when:** Fuzzy search, content search, advanced filters.

### Enhanced Search (M12)
- [ ] Fuzzy matching (typo tolerance)
- [ ] Boolean operators: `upload AND google NOT chrome`
- [ ] Wildcards: `*.py` in searches
- [ ] Regex support: `--regex "pattern"`

### Content Indexing (M13 - Optional)
- [ ] Index file contents (not just metadata)
- [ ] Search inside files: `--in-content "search text"`
- [ ] Configurable: opt-in per directory
- [ ] Exclude sensitive content

### Smart Queries (M14)
- [ ] Saved queries: `config/queries.yaml`
  ```yaml
  queries:
    automation_scripts:
      tags: [automation]
      type: script

    recent_docs:
      type: doc
      modified_after: "7 days ago"
  ```
- [ ] `python -m src.search --saved automation_scripts`

---

## Phase 5 — Integration & Polish (Week 5)

**Done when:** Production-ready with docs and examples.

### CLI Enhancements (M15)
- [ ] Interactive mode: `python -m src.search --interactive`
- [ ] Open file in editor: `python -m src.search "query" --open`
- [ ] Copy path to clipboard: `python -m src.search "query" --copy`
- [ ] JSON output: `python -m src.search "query" --json`

### Documentation (M16)
- [ ] `README.md` — Quick start guide
- [ ] `examples/search_examples.md` — Common queries
- [ ] `examples/tagging_guide.md` — How to tag files
- [ ] `examples/config_guide.md` — Configuration options

### Testing (M17)
- [ ] Unit tests: `tests/test_indexer.py`
- [ ] Integration tests: `tests/test_search.py`
- [ ] Performance tests: Index 10K files in <10 seconds

---

## Future Enhancements (Post-MVP)

### Web UI (V2)
- [ ] Simple Flask app for web-based search
- [ ] Visual file browser
- [ ] Tag cloud visualization
- [ ] File relationship graph

### AI Integration (V3)
- [ ] AI-powered tag suggestions (Claude API)
- [ ] Semantic search (embeddings)
- [ ] Auto-generate descriptions
- [ ] Find similar files

### Collaboration (V4)
- [ ] Export/import index
- [ ] Share tag schemas
- [ ] Team-wide indexing

---

## Out of Scope (Permanent)

- Modifying files (read-only system)
- Version control integration (git handles that)
- File syncing (use existing tools)
- File content editing
- Access control (relies on filesystem permissions)

---

## Success Criteria

**MVP is done when:**
1. ✅ Can index 10K+ files in <30 seconds
2. ✅ Search returns results in <100ms
3. ✅ Find files by name, tags, type, date
4. ✅ Auto-updates when files change
5. ✅ Real problem solved: Can find `GDOCS-UPLOAD-SETUP.md` with query "google docs upload"

**Production-ready when:**
1. ✅ All Phase 1-4 milestones complete
2. ✅ Documentation written
3. ✅ Tests passing
4. ✅ Used daily for 1 week without issues

---

**Created:** 2026-03-20
