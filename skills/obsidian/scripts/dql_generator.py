#!/usr/bin/env python3
"""
Dataview DQL Generator for Obsidian
Generates syntactically correct Dataview Query Language (DQL) blocks
for Map of Content (MOC), Native Tasks, Metadata Tables, Wardrobe Catalogs, and Timeline Rollups.
"""
import sys
import argparse

def gen_moc_table(folder, fields=None, sort_field="file.name ASC"):
    if not fields:
        fields = ['file.link AS "Note"', 'status AS "Status"', 'tags AS "Tags"', 'file.mtime AS "Updated"']
    fields_str = ", ".join(fields)
    return f"""```dataview
TABLE {fields_str}
FROM "{folder}"
SORT {sort_field}
```"""

def gen_task_query(folder=None, tag=None, completed=False):
    from_clause = ""
    if folder and tag:
        from_clause = f'FROM "{folder}" AND {tag}\n'
    elif folder:
        from_clause = f'FROM "{folder}"\n'
    elif tag:
        from_clause = f'FROM {tag}\n'
        
    comp_clause = "completed" if completed else "!completed"
    return f"""```dataview
TASK
{from_clause}WHERE {comp_clause}
GROUP BY file.link
```"""

def gen_wardrobe_table(folder_or_note="04_Fashion_Grooming"):
    if folder_or_note.endswith("Kanad Wardrobe") or folder_or_note.endswith("Kanad Wardrobe.md"):
        return f"""```dataview
TABLE body_measurements.shirt_size AS "Shirt Size", body_measurements.waist_komor AS "Waist", body_measurements.shoe_size_uk AS "Shoe Size (UK)", status AS "Status", last_updated AS "Updated"
FROM "{folder_or_note}"
```"""
    return f"""```dataview
TABLE status AS "Status", tags AS "Tags", type AS "Document Type", last_updated AS "Updated"
FROM "{folder_or_note}"
WHERE type != null
SORT file.name ASC
```"""

def gen_recent_table(folder="", days=7):
    from_clause = f'FROM "{folder}"\n' if folder else ""
    return f"""```dataview
TABLE file.mtime AS "Modified", tags AS "Tags"
{from_clause}WHERE date(today) - file.mtime <= dur({days} days)
SORT file.mtime DESC
LIMIT 15
```"""

def main():
    parser = argparse.ArgumentParser(description="Dataview DQL Query Generator")
    parser.add_argument("type", choices=["moc", "mocs", "task", "tasks", "wardrobe", "recent"], help="Query type to generate")
    parser.add_argument("--folder", default="", help="Folder filter (e.g. 03_Habits_Protocols)")
    parser.add_argument("--tag", default="", help="Tag filter (e.g. #protocol)")
    parser.add_argument("--days", type=int, default=7, help="Number of days for recent files")
    args = parser.parse_args()

    q_type = args.type.rstrip("s") if args.type in ["tasks", "mocs"] else args.type

    if q_type == "moc":
        folder = args.folder or "00_Dashboard"
        print(gen_moc_table(folder))
    elif q_type == "task":
        print(gen_task_query(args.folder, args.tag))
    elif q_type == "wardrobe":
        note = args.folder or "04_Fashion_Grooming"
        print(gen_wardrobe_table(note))
    elif q_type == "recent":
        print(gen_recent_table(args.folder, args.days))

if __name__ == "__main__":
    main()
