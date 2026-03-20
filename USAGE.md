# Usage Guide — File Index

Quick reference for using the file index system.

---

## First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Build the index (configure directories in config/directories.yaml first)
python -m src.indexer
```

This scans all configured directories and builds a DuckDB index. Takes 20-30 seconds for 2000+ files.

---

## Searching

**Basic text search:**
```bash
python -m src.search "deployment"
```
Searches in: filename, path, description, and tags.

**Filter by tag:**
```bash
python -m src.search --tag automation
```

**Filter by file type:**
```bash
python -m src.search --type script
python -m src.search --type doc
python -m src.search --type config
```

**Filter by category:**
```bash
python -m src.search --category projects
python -m src.search --category research
```

**Filter by date:**
```bash
python -m src.search --modified-after 2026-03-15
```

**Combine filters:**
```bash
python -m src.search --tag automation --type script --category projects
python -m src.search "database" --type doc --modified-after 2026-03-01
```

**Limit results:**
```bash
python -m src.search "query" --limit 20  # Default is 10
```

**Show statistics:**
```bash
python -m src.search --stats
```

---

## Rebuilding the Index

When files change, rebuild the index:

```bash
python -m src.indexer
```

This re-scans all configured directories and updates the index.

**Dry run (preview without writing):**
```bash
python -m src.indexer --dry-run
```

---

## Configuration

**Directories:** Edit `config/directories.yaml`
```yaml
directories:
  - path: /path/to/your/projects
    category: projects
    exclude:
      - "**/.git/**"
      - "**/__pycache__/**"
      - "**/node_modules/**"
```

**Tags:** Edit `config/tags.yaml`
```yaml
auto_tags:
  extensions:
    ".py": [script, python]
    ".md": [doc, markdown]
  directories:
    scripts: [script, automation]
    docs: [documentation]
```

---

## File Tags

**Auto-tagged based on:**
- File extension (`.py` → python, script)
- Directory name (`scripts/` → script, automation)
- Manual tags in files (see below)

**Add manual tags to files:**

Python files:
```python
# tags: automation, important, production
# description: Does something important
```

Markdown files:
```markdown
---
tags: [documentation, setup, guide]
description: Setup guide for deployment
---
```

---

## Performance

- **Indexing:** ~20-30 seconds for 2000 files
- **Search:** <100ms for most queries
- **Database:** Single file (`file_index.duckdb`)

---

## Troubleshooting

**Index not found:**
```
Run: python -m src.indexer
```

**Search returns no results:**
- Check if index is built
- Try broader search terms
- Use `--stats` to see what's in the index

**Slow performance:**
- Check database file size
- Consider excluding large directories

---

**Created:** 2026-03-20
