#!/usr/bin/env python3
"""
Zotero Study & Library Manager CLI
Query local Zotero SQLite library (collections, items, attachments, tags).
Supports locating study PDFs (RRB, SSC, Banking, Books), extracting metadata,
and exporting summaries for Obsidian.
"""

import sys
import os
import sqlite3
import json
import argparse
import shutil
import tempfile
import atexit

ZOTERO_DIR = os.path.expanduser('~/Zotero')
DB_PATH = os.path.join(ZOTERO_DIR, 'zotero.sqlite')
STORAGE_DIR = os.path.join(ZOTERO_DIR, 'storage')

_SNAP_DIRS = []

def _cleanup_snaps():
    for d in _SNAP_DIRS:
        shutil.rmtree(d, ignore_errors=True)

atexit.register(_cleanup_snaps)

def get_db():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, timeout=0.5)
        conn.execute("SELECT 1 FROM items LIMIT 1;")
        return conn
    except sqlite3.OperationalError:
        # Zotero Desktop holds a live WAL lock; snapshot sqlite + wal/shm atomically for lock-free read
        snap_dir = tempfile.mkdtemp(prefix="zotero_ro_snap_")
        _SNAP_DIRS.append(snap_dir)
        for suffix in ("", "-wal", "-shm"):
            src = DB_PATH + suffix
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(snap_dir, "zotero.sqlite" + suffix))
        return sqlite3.connect(os.path.join(snap_dir, "zotero.sqlite"), timeout=5)

def list_collections():
    conn = get_db()
    c = conn.cursor()
    query = """
    SELECT c.collectionID, c.collectionName, c.parentCollectionID, COUNT(ci.itemID) as count
    FROM collections c
    LEFT JOIN collectionItems ci ON c.collectionID = ci.collectionID
    GROUP BY c.collectionID
    ORDER BY c.collectionName ASC;
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()

    collections = []
    for cid, name, parent_id, count in rows:
        collections.append({
            "id": cid,
            "name": name,
            "parentId": parent_id,
            "itemCount": count
        })
    return collections

def search_items(query_str=None, collection_name=None, limit=50):
    conn = get_db()
    c = conn.cursor()

    conditions = ["i.itemID NOT IN (SELECT itemID FROM deletedItems)"]
    params = []

    if collection_name:
        conditions.append("""i.itemID IN (
            SELECT ci.itemID FROM collectionItems ci
            JOIN collections c ON ci.collectionID = c.collectionID
            WHERE c.collectionName LIKE ?
        )""")
        params.append(f"%{collection_name}%")

    sql = f"""
    SELECT DISTINCT i.itemID, i.key, it.typeName,
        (SELECT v.value FROM itemData id
         JOIN itemDataValues v ON id.valueID = v.valueID
         JOIN fields f ON id.fieldID = f.fieldID
         WHERE id.itemID = i.itemID AND f.fieldName = 'title' LIMIT 1) as title,
        (SELECT v.value FROM itemData id
         JOIN itemDataValues v ON id.valueID = v.valueID
         JOIN fields f ON id.fieldID = f.fieldID
         WHERE id.itemID = i.itemID AND f.fieldName = 'date' LIMIT 1) as date
    FROM items i
    JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
    WHERE {' AND '.join(conditions)}
    """

    if query_str:
        sql += """ AND (
            title LIKE ? OR i.key LIKE ?
        )"""
        params.extend([f"%{query_str}%", f"%{query_str}%"])

    sql += f" ORDER BY i.itemID DESC LIMIT {int(limit)}"

    c.execute(sql, params)
    rows = c.fetchall()

    results = []
    for item_id, key, item_type, title, date in rows:
        # Check attachment path
        c.execute("""
            SELECT att_item.key, ia.path, ia.contentType
            FROM itemAttachments ia
            JOIN items att_item ON ia.itemID = att_item.itemID
            WHERE ia.parentItemID = ? OR ia.itemID = ?
        """, (item_id, item_id))
        att = c.fetchone()
        file_path = None
        if att:
            att_key, att_path, content_type = att
            if att_path and att_path.startswith("storage:"):
                fname = att_path.replace("storage:", "")
                candidate = os.path.join(STORAGE_DIR, att_key, fname)
                if os.path.exists(candidate):
                    file_path = candidate

        results.append({
            "id": item_id,
            "key": key,
            "type": item_type,
            "title": title or "Untitled",
            "date": date or "",
            "filePath": file_path
        })

    conn.close()
    return results

def get_item(item_key_or_id):
    conn = get_db()
    c = conn.cursor()

    is_id = str(item_key_or_id).isdigit()
    where_clause = "i.itemID = ?" if is_id else "i.key = ?"
    param = int(item_key_or_id) if is_id else str(item_key_or_id)

    c.execute(f"""
        SELECT i.itemID, i.key, it.typeName
        FROM items i
        JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
        WHERE {where_clause}
    """, (param,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None

    item_id, key, item_type = row

    # Fetch fields
    c.execute("""
        SELECT f.fieldName, v.value
        FROM itemData id
        JOIN fields f ON id.fieldID = f.fieldID
        JOIN itemDataValues v ON id.valueID = v.valueID
        WHERE id.itemID = ?
    """, (item_id,))
    fields = dict(c.fetchall())

    # Fetch collections
    c.execute("""
        SELECT c.collectionName
        FROM collectionItems ci
        JOIN collections c ON ci.collectionID = c.collectionID
        WHERE ci.itemID = ?
    """, (item_id,))
    collections = [r[0] for r in c.fetchall()]

    # Fetch attachment
    c.execute("""
        SELECT att_item.key, ia.path, ia.contentType
        FROM itemAttachments ia
        JOIN items att_item ON ia.itemID = att_item.itemID
        WHERE ia.parentItemID = ? OR ia.itemID = ?
    """, (item_id, item_id))
    att = c.fetchone()
    file_path = None
    if att:
        att_key, att_path, ctype = att
        if att_path and att_path.startswith("storage:"):
            fname = att_path.replace("storage:", "")
            candidate = os.path.join(STORAGE_DIR, att_key, fname)
            if os.path.exists(candidate):
                file_path = candidate

    conn.close()

    return {
        "id": item_id,
        "key": key,
        "type": item_type,
        "collections": collections,
        "fields": fields,
        "filePath": file_path
    }

def main():
    parser = argparse.ArgumentParser(description="Zotero Study & Library CLI")
    subparsers = parser.add_subparsers(dest="command")

    # collections
    subparsers.add_parser("collections", help="List all Zotero collections with counts")

    # search
    search_p = subparsers.add_parser("search", help="Search Zotero items")
    search_p.add_argument("query", nargs="?", default="", help="Search query (title, author, key)")
    search_p.add_argument("--collection", "-c", help="Filter by collection name")
    search_p.add_argument("--limit", "-l", type=int, default=30, help="Max items to return")
    search_p.add_argument("--json", action="store_true", help="Output JSON format")

    # get
    get_p = subparsers.add_parser("get", help="Get item details and attachment path")
    get_p.add_argument("key_or_id", help="Item ID or Zotero 8-character Key")
    get_p.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    if args.command == "collections":
        cols = list_collections()
        print(f"{'ID':<6} | {'Count':<6} | {'Collection Name'}")
        print("-" * 50)
        for col in cols:
            print(f"{col['id']:<6} | {col['itemCount']:<6} | {col['name']}")

    elif args.command == "search":
        items = search_items(args.query, args.collection, args.limit)
        if args.json:
            print(json.dumps(items, indent=2))
        else:
            print(f"Found {len(items)} items:")
            for item in items:
                has_file = "📎 PDF" if item['filePath'] else "      "
                print(f"[{item['key']}] {has_file} {item['title'][:70]}")
                if item['filePath']:
                    print(f"       -> Path: {item['filePath']}")

    elif args.command == "get":
        item = get_item(args.key_or_id)
        if not item:
            print(f"Item not found: {args.key_or_id}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(item, indent=2))
        else:
            print(f"Title:       {item['fields'].get('title', 'N/A')}")
            print(f"Key:         {item['key']} (ID: {item['id']})")
            print(f"Type:        {item['type']}")
            print(f"Collections: {', '.join(item['collections'])}")
            if item['filePath']:
                print(f"File Path:   {item['filePath']}")
            print("Fields:")
            for k, v in item['fields'].items():
                print(f"  {k}: {v}")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
