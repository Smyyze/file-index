"""
CLI search tool for the file index.

Usage:
    python -m src.search "google docs"               # Text search
    python -m src.search --tag automation            # Filter by tag
    python -m src.search --type script               # Filter by type
    python -m src.search --category projects         # Filter by category
    python -m src.search --modified-after 2026-03-01 # Date range
    python -m src.search --limit 20                  # Limit results
    python -m src.search --stats                     # Show index stats
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import duckdb
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

DB_PATH = Path(__file__).parent.parent / "file_index.duckdb"


def build_query(
    query: str | None,
    tag: str | None,
    type_: str | None,
    category: str | None,
    modified_after: str | None,
    limit: int,
) -> tuple[str, list]:
    conditions = []
    params = []

    if query:
        # Search name, description, and tags (cast tags array to string)
        conditions.append("""
            (
                name ILIKE ?
                OR description ILIKE ?
                OR array_to_string(tags, ' ') ILIKE ?
                OR path ILIKE ?
            )
        """)
        q = f"%{query}%"
        params.extend([q, q, q, q])

    if tag:
        conditions.append("list_contains(tags, ?)")
        params.append(tag)

    if type_:
        conditions.append("type = ?")
        params.append(type_)

    if category:
        conditions.append("category = ?")
        params.append(category)

    if modified_after:
        try:
            dt = datetime.fromisoformat(modified_after)
            conditions.append("modified >= ?")
            params.append(dt)
        except ValueError:
            console.print(f"[red]Invalid date format:[/] {modified_after} (use YYYY-MM-DD)")
            sys.exit(1)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    sql = f"""
        SELECT name, path, type, category, tags, description, quick_command, modified, size_kb
        FROM file_index
        {where}
        ORDER BY modified DESC
        LIMIT {limit}
    """
    return sql, params


def display_results(rows: list, query: str | None) -> None:
    if not rows:
        console.print("[yellow]No results found.[/]")
        return

    console.print(f"\n[bold green]{len(rows)} result(s)[/]\n")

    for i, row in enumerate(rows, 1):
        name, path, type_, category, tags, description, quick_command, modified, size_kb = row

        tags_str = ", ".join(tags) if tags else "—"
        mod_str = modified.strftime("%Y-%m-%d") if modified else "—"
        size_str = f"{size_kb:.1f} KB" if size_kb is not None else "—"

        console.print(f"[bold cyan]{i}. {name}[/]  [dim]{type_ or ''}  {size_str}  {mod_str}[/]")
        console.print(f"   [dim]Path:[/] {path}")
        if description:
            console.print(f"   [dim]Desc:[/] {description}")
        console.print(f"   [dim]Tags:[/] {tags_str}")
        if quick_command:
            console.print(f"   [dim]Cmd :[/] [green]{quick_command}[/]")
        console.print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the file index")
    parser.add_argument("query", nargs="?", help="Text to search (name, description, tags, path)")
    parser.add_argument("--tag", "-t", metavar="TAG", help="Filter by tag")
    parser.add_argument("--type", "-T", metavar="TYPE", dest="type_", help="Filter by type (script/doc/config/data)")
    parser.add_argument("--category", "-c", metavar="CAT", help="Filter by category (projects/life-ops/research)")
    parser.add_argument("--modified-after", "-m", metavar="DATE", help="Only files modified after date (YYYY-MM-DD)")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--stats", action="store_true", help="Show index statistics")
    args = parser.parse_args()

    if not DB_PATH.exists():
        console.print("[red]Index not found.[/] Run [bold]python -m src.indexer[/] first.")
        sys.exit(1)

    conn = duckdb.connect(str(DB_PATH), read_only=True)

    if args.stats:
        from src.indexer import show_stats
        show_stats(conn)
        conn.close()
        return

    if not any([args.query, args.tag, args.type_, args.category, args.modified_after]):
        parser.print_help()
        sys.exit(0)

    sql, params = build_query(
        args.query, args.tag, args.type_, args.category, args.modified_after, args.limit
    )

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    display_results(rows, args.query)


if __name__ == "__main__":
    main()
