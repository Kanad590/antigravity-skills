#!/usr/bin/env python3
"""
Calibre Library Management Helper CLI
Interfaces with calibredb to manage /home/saman/Calibre Library.
Supports searching, metadata inspection, format verification, adding new books,
and running curation workflows.
"""

import sys
import os
import subprocess
import json
import argparse

LIBRARY_PATH = os.path.expanduser('~/Calibre Library')

def run_calibredb(args):
    cmd = ["calibredb"] + args + ["--library-path", LIBRARY_PATH]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"calibredb error: {res.stderr.strip()}", file=sys.stderr)
        return None
    return res.stdout

def list_books(search_query=None, limit=50, sort_by="id"):
    args = ["list", "--fields", "id,title,authors,formats,tags", "--sort-by", sort_by, "--limit", str(limit)]
    if search_query:
        args.extend(["--search", search_query])
    
    # Run with json output
    cmd = ["calibredb", "list", "--fields", "id,title,authors,formats,tags", "--for-machine", "--library-path", LIBRARY_PATH]
    if search_query:
        cmd.extend(["--search", search_query])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return []
    try:
        data = json.loads(res.stdout)
        return data[:limit]
    except Exception:
        return []

def show_metadata(book_id):
    out = run_calibredb(["show_metadata", str(book_id)])
    return out

def add_book(file_path, tags=None, authors=None, title=None):
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at {file_path}", file=sys.stderr)
        return False
    args = ["add", file_path]
    if tags:
        args.extend(["--tags", tags])
    if authors:
        args.extend(["--authors", authors])
    if title:
        args.extend(["--title", title])
    out = run_calibredb(args)
    if out is not None:
        print(out)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Calibre Library Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # list
    list_p = subparsers.add_parser("list", help="List or search books in Calibre Library")
    list_p.add_argument("query", nargs="?", default=None, help="Search query (e.g. author:\"...\" or title keywords)")
    list_p.add_argument("--limit", "-l", type=int, default=30, help="Max books to show")
    list_p.add_argument("--json", action="store_true", help="Output JSON format")

    # show
    show_p = subparsers.add_parser("show", help="Show detailed metadata for a book")
    show_p.add_argument("book_id", type=int, help="Calibre Book ID")

    # add
    add_p = subparsers.add_parser("add", help="Add a book file to Calibre Library")
    add_p.add_argument("file_path", help="Path to PDF/EPUB/MOBI file")
    add_p.add_argument("--tags", help="Comma-separated tags")
    add_p.add_argument("--authors", help="Author name(s)")
    add_p.add_argument("--title", help="Custom Title")

    args = parser.parse_args()

    if args.command == "list":
        books = list_books(args.query, args.limit)
        if args.json:
            print(json.dumps(books, indent=2))
        else:
            print(f"Found {len(books)} books:")
            print(f"{'ID':<6} | {'Authors':<25} | {'Title'}")
            print("-" * 75)
            for b in books:
                raw_authors = b.get("authors", "")
                authors = raw_authors if isinstance(raw_authors, str) else ", ".join(raw_authors)
                title = b.get("title", "")[:40]
                print(f"{b.get('id', ''):<6} | {authors[:25]:<25} | {title}")

    elif args.command == "show":
        meta = show_metadata(args.book_id)
        if meta:
            print(meta)

    elif args.command == "add":
        add_book(args.file_path, args.tags, args.authors, args.title)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
