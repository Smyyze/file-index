"""
File indexer — scans configured directories and builds a DuckDB index.

Usage:
    python -m src.indexer                    # Full index (all directories)
    python -m src.indexer --update           # Re-scan all (same as above)
    python -m src.indexer --file <path>      # Re-index a single file
    python -m src.indexer --dir <path>       # Index one specific directory
    python -m src.indexer --dry-run          # Preview without writing
    python -m src.indexer --stats            # Show index statistics
"""

import argparse
import fnmatch
import os
import sys
from datetime import datetime
from pathlib import Path

import duckdb
import yaml
from rich.console import Console
from rich.progress import BarColumn, Progress, MofNCompleteColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from src.schema import init_schema

console = Console(highlight=False)

DB_PATH = Path(__file__).parent.parent / "file_index.duckdb"
CONFIG_DIR = Path(__file__).parent.parent / "config"
DIRECTORIES_CONFIG = CONFIG_DIR / "directories.yaml"
TAGS_CONFIG = CONFIG_DIR / "tags.yaml"


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_directories_config() -> list[dict]:
    with open(DIRECTORIES_CONFIG) as f:
        data = yaml.safe_load(f)
    return data.get("directories", [])


def load_tags_config() -> dict:
    with open(TAGS_CONFIG) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Tag derivation
# ---------------------------------------------------------------------------

def derive_tags(path: Path, category: str, tags_cfg: dict) -> list[str]:
    tags = set()
    auto = tags_cfg.get("auto_tags", {})

    # Category tag
    if category:
        tags.add(category)

    # Extension tags
    ext_tags = auto.get("extensions", {})
    ext = path.suffix.lower()
    for t in ext_tags.get(ext, []):
        tags.add(t)

    # Directory-name tags (any part of the path)
    dir_tags = auto.get("directories", {})
    for part in path.parts:
        for dir_name, dtags in dir_tags.items():
            if part.lower() == dir_name.lower():
                for t in dtags:
                    tags.add(t)

    return sorted(tags)


def read_inline_tags(path: Path) -> tuple[list[str], str | None]:
    """Read tags/description from file comments or YAML frontmatter."""
    tags: list[str] = []
    description: str | None = None

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return tags, description

    lines = text.splitlines()

    # YAML frontmatter (markdown)
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end:
            try:
                fm = yaml.safe_load("\n".join(lines[1:end]))
                if isinstance(fm, dict):
                    if "tags" in fm:
                        raw = fm["tags"]
                        tags = raw if isinstance(raw, list) else [t.strip() for t in str(raw).split(",")]
                    if "description" in fm:
                        description = str(fm["description"])
            except Exception:
                pass
            return tags, description

    # Inline comments (Python / shell / yaml)
    for line in lines[:30]:
        stripped = line.strip().lstrip("#").strip()
        if stripped.lower().startswith("tags:"):
            raw = stripped[5:].strip()
            tags = [t.strip() for t in raw.split(",") if t.strip()]
        elif stripped.lower().startswith("description:"):
            description = stripped[12:].strip()

    return tags, description


def classify_type(path: Path, tags: list[str]) -> str:
    if "script" in tags:
        return "script"
    if "doc" in tags or "markdown" in tags:
        return "doc"
    if "config" in tags:
        return "config"
    if "data" in tags:
        return "data"
    return "other"


# ---------------------------------------------------------------------------
# Path exclusion
# ---------------------------------------------------------------------------

def is_excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    rel = path.relative_to(root).as_posix()
    for pattern in patterns:
        # Strip leading **/ for simple matching
        clean = pattern.lstrip("*").lstrip("/")
        if fnmatch.fnmatch(rel, pattern):
            return True
        # Check each part of the path
        for part in path.parts:
            if fnmatch.fnmatch(part, clean.strip("/")):
                return True
    return False


# ---------------------------------------------------------------------------
# File record building
# ---------------------------------------------------------------------------

def build_record(path: Path, category: str, tags_cfg: dict) -> dict | None:
    try:
        stat = path.stat()
    except Exception:
        return None

    auto_tags = derive_tags(path, category, tags_cfg)
    inline_tags, description = read_inline_tags(path)

    all_tags = sorted(set(auto_tags + inline_tags))

    return {
        "name": path.name,
        "path": str(path).replace("\\", "/"),
        "type": classify_type(path, all_tags),
        "category": category,
        "tags": all_tags,
        "description": description,
        "quick_command": None,
        "related_files": [],
        "created": datetime.fromtimestamp(stat.st_ctime),
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "size_kb": round(stat.st_size / 1024, 2),
    }


# ---------------------------------------------------------------------------
# Upsert
# ---------------------------------------------------------------------------

def upsert_record(conn: duckdb.DuckDBPyConnection, rec: dict) -> None:
    conn.execute("""
        INSERT INTO file_index
            (name, path, type, category, tags, description,
             quick_command, related_files, created, modified, size_kb)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (path) DO UPDATE SET
            name          = excluded.name,
            type          = excluded.type,
            category      = excluded.category,
            tags          = excluded.tags,
            description   = COALESCE(excluded.description, file_index.description),
            quick_command = COALESCE(file_index.quick_command, excluded.quick_command),
            related_files = excluded.related_files,
            modified      = excluded.modified,
            size_kb       = excluded.size_kb
    """, [
        rec["name"], rec["path"], rec["type"], rec["category"],
        rec["tags"], rec["description"], rec["quick_command"],
        rec["related_files"], rec["created"], rec["modified"], rec["size_kb"],
    ])


def remove_deleted(conn: duckdb.DuckDBPyConnection) -> int:
    """Remove index entries whose files no longer exist."""
    paths = conn.execute("SELECT path FROM file_index").fetchall()
    removed = 0
    for (p,) in paths:
        if not Path(p).exists():
            conn.execute("DELETE FROM file_index WHERE path = ?", [p])
            removed += 1
    return removed


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".pdf", ".docx", ".xlsx", ".pptx", ".odt",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".db", ".duckdb", ".sqlite",
    ".pyc", ".pyo", ".pyd",
}


def should_index(path: Path) -> bool:
    return path.suffix.lower() not in BINARY_EXTENSIONS


def scan_directory(
    dir_cfg: dict,
    tags_cfg: dict,
    dry_run: bool,
    conn: duckdb.DuckDBPyConnection,
    progress: Progress,
    task_id,
) -> tuple[int, int]:
    root = Path(dir_cfg["path"])
    category = dir_cfg.get("category", "unknown")
    exclude_patterns = dir_cfg.get("exclude", [])

    if not root.exists():
        console.print(f"[yellow]Warning:[/] Directory not found: {root}")
        return 0, 0

    indexed = 0
    skipped = 0

    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)

        # Prune excluded directories in-place
        dirnames[:] = [
            d for d in dirnames
            if not is_excluded(current / d, root, exclude_patterns)
        ]

        for fname in filenames:
            fpath = current / fname

            if is_excluded(fpath, root, exclude_patterns):
                skipped += 1
                continue

            if not should_index(fpath):
                skipped += 1
                continue

            rec = build_record(fpath, category, tags_cfg)
            if rec is None:
                skipped += 1
                continue

            if not dry_run:
                upsert_record(conn, rec)

            indexed += 1
            progress.advance(task_id)
            progress.update(task_id, description=f"[cyan]{category}[/] {fname[:50]}")

    return indexed, skipped


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="File indexer — build and update the DuckDB file index")
    parser.add_argument("--update", action="store_true", help="Re-scan all directories (default behavior)")
    parser.add_argument("--file", metavar="PATH", help="Re-index a single file")
    parser.add_argument("--dir", metavar="PATH", help="Index one specific directory (overrides config)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing to DB")
    parser.add_argument("--stats", action="store_true", help="Show index statistics and exit")
    args = parser.parse_args()

    conn = duckdb.connect(str(DB_PATH))
    init_schema(conn)

    if args.stats:
        show_stats(conn)
        conn.close()
        return

    tags_cfg = load_tags_config()

    # Single file mode
    if args.file:
        path = Path(args.file)
        if not path.exists():
            console.print(f"[red]File not found:[/] {path}")
            sys.exit(1)
        rec = build_record(path, "manual", tags_cfg)
        if rec and not args.dry_run:
            upsert_record(conn, rec)
            console.print(f"[green]Indexed:[/] {path}")
        elif rec:
            console.print(f"[yellow]Dry run:[/] would index {path} tags={rec['tags']}")
        conn.close()
        return

    # Directory override mode
    if args.dir:
        dir_cfgs = [{"path": args.dir, "category": "manual", "exclude": []}]
    else:
        dir_cfgs = load_directories_config()

    if args.dry_run:
        console.print("[yellow]DRY RUN — no changes will be written[/]")

    total_indexed = 0
    total_skipped = 0

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        for dir_cfg in dir_cfgs:
            task_id = progress.add_task(f"[cyan]{dir_cfg['category']}[/] scanning…", total=None)
            indexed, skipped = scan_directory(dir_cfg, tags_cfg, args.dry_run, conn, progress, task_id)
            total_indexed += indexed
            total_skipped += skipped
            progress.update(task_id, description=f"[green]{dir_cfg['category']}[/] done ({indexed} files)")

    if not args.dry_run:
        removed = remove_deleted(conn)
        if removed:
            console.print(f"[yellow]Removed {removed} stale entries[/]")

    conn.close()

    console.print()
    console.print(f"[bold green]Done.[/] Indexed [bold]{total_indexed}[/] files, skipped {total_skipped}.")
    if args.dry_run:
        console.print("[yellow](Dry run — nothing written)[/]")


def show_stats(conn: duckdb.DuckDBPyConnection) -> None:
    total = conn.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
    by_category = conn.execute(
        "SELECT category, COUNT(*) FROM file_index GROUP BY category ORDER BY 2 DESC"
    ).fetchall()
    by_type = conn.execute(
        "SELECT type, COUNT(*) FROM file_index GROUP BY type ORDER BY 2 DESC"
    ).fetchall()

    console.print(f"\n[bold]File Index Stats[/] — {total} total files\n")

    t = Table(title="By Category")
    t.add_column("Category")
    t.add_column("Files", justify="right")
    for row in by_category:
        t.add_row(row[0] or "—", str(row[1]))
    console.print(t)

    t2 = Table(title="By Type")
    t2.add_column("Type")
    t2.add_column("Files", justify="right")
    for row in by_type:
        t2.add_row(row[0] or "—", str(row[1]))
    console.print(t2)


if __name__ == "__main__":
    main()
