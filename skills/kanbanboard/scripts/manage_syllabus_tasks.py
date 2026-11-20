#!/usr/bin/env python3
"""
Syllabus Tracker Helper for Project #5: All Subjects Syllabus Tracker 📋
"""
import sys
import os
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from kanban_cli import call_rpc

PROJECT_ID = 5

LEVELS = [
    ("Level 0", "📥 Backlog (Uncovered)"),
    ("Level 1", "🧠 Concept Clear"),
    ("Level 2", "💪 Strong Level 1 (Need to work)"),
    ("Level 3", "🔥 Strong Level 2 (Building Confidence)"),
    ("Level 4", "🚀 Strong Level 3 (Exam Ready)"),
    ("Level 5", "🏆 Strong Level 4 (Mastered)")
]

def get_columns_map():
    cols = call_rpc("getColumns", {"project_id": PROJECT_ID})
    title_to_id = {c["title"]: c["id"] for c in cols}
    id_to_title = {c["id"]: c["title"] for c in cols}
    return title_to_id, id_to_title

def cmd_progress(args):
    """Show mastery breakdown by subject category."""
    title_to_id, id_to_title = get_columns_map()
    tasks = call_rpc("getAllTasks", {"project_id": PROJECT_ID, "status_id": 1})
    categories = call_rpc("getAllCategories", {"project_id": PROJECT_ID})
    cat_map = {c["id"]: c["name"] for c in categories}
    cat_map[0] = "Uncategorized"
    
    # Structure: {cat_name: {level_title: count}}
    cat_stats = {name: {title: 0 for _, title in LEVELS} for name in cat_map.values()}
    
    for t in tasks:
        cat_name = cat_map.get(t.get("category_id", 0), "Uncategorized")
        col_title = id_to_title.get(t["column_id"], "Unknown")
        if cat_name in cat_stats and col_title in cat_stats[cat_name]:
            cat_stats[cat_name][col_title] += 1
            
    print("=" * 80)
    print("        📚 SYLLABUS MASTERY PROGRESS REPORT BY SUBJECT")
    print("=" * 80)
    
    total_mastered = sum(t["column_id"] == title_to_id.get("🏆 Strong Level 4 (Mastered)", -1) for t in tasks)
    total_ready = sum(t["column_id"] == title_to_id.get("🚀 Strong Level 3 (Exam Ready)", -1) for t in tasks)
    print(f"Total Topics: {len(tasks)} | 🏆 Mastered: {total_mastered} | 🚀 Exam Ready: {total_ready}")
    print("-" * 80)
    
    for cat_name, stats in sorted(cat_stats.items()):
        cat_total = sum(stats.values())
        if cat_total == 0:
            continue
        mastered = stats.get("🏆 Strong Level 4 (Mastered)", 0)
        ready = stats.get("🚀 Strong Level 3 (Exam Ready)", 0)
        l2 = stats.get("🔥 Strong Level 2 (Building Confidence)", 0)
        backlog = stats.get("📥 Backlog (Uncovered)", 0)
        pct = int(((mastered + ready) / cat_total) * 100) if cat_total > 0 else 0
        
        print(f"\n{cat_name} (Total: {cat_total} | Ready/Mastered: {pct}%)")
        print(f"  • Backlog: {backlog:>2} | Working: {cat_total - backlog - ready - mastered:>2} | Ready: {ready:>2} | Mastered: {mastered:>2}")
    print("\n" + "=" * 80)

def cmd_search(args):
    """Search topics by keyword."""
    title_to_id, id_to_title = get_columns_map()
    tasks = call_rpc("searchTasks", {"project_id": PROJECT_ID, "query": f"status:open {args.query}"})
    categories = call_rpc("getAllCategories", {"project_id": PROJECT_ID})
    cat_map = {c["id"]: c["name"] for c in categories}
    
    print(f"Found {len(tasks)} topic(s) matching '{args.query}':")
    print("-" * 75)
    for t in tasks:
        col = id_to_title.get(t["column_id"], "Unknown")
        cat = cat_map.get(t.get("category_id", 0), "")
        print(f"• #{t['id']:<4} [{col}] {t['title']}")
        if cat:
            print(f"       Category: {cat}")

def cmd_promote(args):
    """Promote topic to next mastery level."""
    title_to_id, id_to_title = get_columns_map()
    task = call_rpc("getTask", {"task_id": args.task_id})
    if not task:
        print(f"❌ Task #{args.task_id} not found.", file=sys.stderr)
        sys.exit(1)
        
    current_col = id_to_title.get(task["column_id"])
    ordered_titles = [title for _, title in LEVELS]
    
    try:
        idx = ordered_titles.index(current_col)
    except ValueError:
        idx = 0
        
    if idx >= len(ordered_titles) - 1:
        print(f"🏆 Task #{args.task_id} ('{task['title']}') is already at the highest mastery level: '{current_col}'!")
        return
        
    next_col_title = ordered_titles[idx + 1]
    next_col_id = title_to_id[next_col_title]
    
    res = call_rpc("moveTaskPosition", {
        "project_id": PROJECT_ID,
        "task_id": args.task_id,
        "column_id": next_col_id,
        "position": 1,
        "swimlane_id": task.get("swimlane_id", 0)
    })
    
    if res:
        print(f"🎉 Promoted Topic #{args.task_id} ('{task['title']}'):")
        print(f"   {current_col}  ➔  {next_col_title}")
    else:
        print(f"❌ Failed to promote task #{args.task_id}")

def main():
    parser = argparse.ArgumentParser(description="Syllabus Tracker Management Helper")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    sub_prog = subparsers.add_parser("progress", help="Show syllabus mastery breakdown by subject")
    sub_prog.set_defaults(func=cmd_progress)
    
    sub_search = subparsers.add_parser("search", help="Search syllabus topics")
    sub_search.add_argument("query", type=str, help="Search term (e.g. 'Harappa', 'Trigonometry')")
    sub_search.set_defaults(func=cmd_search)
    
    sub_promote = subparsers.add_parser("promote", help="Promote topic to next mastery stage")
    sub_promote.add_argument("task_id", type=int, help="Task ID")
    sub_promote.set_defaults(func=cmd_promote)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
