#!/usr/bin/env python3
"""
Exam Tracker Helper for Project #4: 🎯 Govt Exam Tracker (Auto)
"""
import sys
import os
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from kanban_cli import call_rpc

PROJECT_ID = 4

# Ordered Lifecycle Stages
STAGES = [
    "📥 To Apply",
    "🟢 Application Ongoing",
    "📝 Applied",
    "🗺️ City Slip Out",
    "🎫 Admit Card Out",
    "💻 CBT 1 Done",
    "⏳ Awaiting CBT 1 Result",
    "✅ CBT 1 Qualified",
    "🎫 CBT 2 Admit Out",
    "🧪 CBT 2 Done",
    "⏳ Awaiting CBT 2 Result",
    "✅ CBT 2 Qualified",
    "👨‍💼 DV/Interview Scheduled",
    "🪪 DV/Interview Done",
    "⏳ Final Result Awaited",
    "🎉 Selected",
    "❌ Not Selected",
    "🚫 Cancelled/Postponed"
]

def get_columns_map():
    cols = call_rpc("getColumns", {"project_id": PROJECT_ID})
    title_to_id = {c["title"]: c["id"] for c in cols}
    id_to_title = {c["id"]: c["title"] for c in cols}
    return title_to_id, id_to_title

def cmd_list(args):
    title_to_id, id_to_title = get_columns_map()
    tasks = call_rpc("getAllTasks", {"project_id": PROJECT_ID, "status_id": 1})
    
    # Group tasks by stage
    by_stage = {}
    for t in tasks:
        stage = id_to_title.get(t["column_id"], "Unknown")
        by_stage.setdefault(stage, []).append(t)
        
    print("=" * 70)
    print("           🎯 GOVT EXAM TRACKER — ACTIVE EXAMS BY STAGE")
    print("=" * 70)
    for stage in STAGES:
        items = by_stage.get(stage, [])
        if items:
            print(f"\n{stage} ({len(items)}):")
            for t in items:
                due = ""
                if t.get("date_due") and int(t["date_due"]) > 0:
                    due = f" [Due: {datetime.fromtimestamp(int(t['date_due'])).strftime('%Y-%m-%d')}]"
                print(f"  • #{t['id']:<3} {t['title']}{due}")
    print("\n" + "=" * 70)

def cmd_set_stage(args):
    title_to_id, id_to_title = get_columns_map()
    target_stage = None
    for s in STAGES:
        if args.stage.lower().strip() in s.lower():
            target_stage = s
            break
            
    if not target_stage:
        print(f"❌ Unknown stage: '{args.stage}'", file=sys.stderr)
        print("Available stages:")
        for s in STAGES:
            print(f"  • {s}")
        sys.exit(1)
        
    task = call_rpc("getTask", {"task_id": args.task_id})
    if not task:
        print(f"❌ Task #{args.task_id} not found.", file=sys.stderr)
        sys.exit(1)
        
    old_stage = id_to_title.get(task["column_id"], "Unknown")
    new_col_id = title_to_id[target_stage]
    
    res = call_rpc("moveTaskPosition", {
        "project_id": PROJECT_ID,
        "task_id": args.task_id,
        "column_id": new_col_id,
        "position": 1,
        "swimlane_id": task.get("swimlane_id", 0)
    })
    
    if res:
        print(f"✅ Moved Exam #{args.task_id} ('{task['title']}'):")
        print(f"   {old_stage}  ➔  {target_stage}")
        if args.comment:
            call_rpc("createComment", {
                "task_id": args.task_id,
                "user_id": 2,
                "content": f"🤖 {args.comment}"
            })
            print(f"   Added AI comment: '{args.comment}'")
    else:
        print(f"❌ Failed to move Task #{args.task_id}")

def main():
    parser = argparse.ArgumentParser(description="Exam Tracker Management Helper")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    sub_list = subparsers.add_parser("list", help="List all exams grouped by stage")
    sub_list.set_defaults(func=cmd_list)
    
    sub_stage = subparsers.add_parser("set-stage", help="Move exam to a new stage")
    sub_stage.add_argument("task_id", type=int, help="Task ID")
    sub_stage.add_argument("stage", type=str, help="Stage name (e.g. 'Admit Card Out', 'CBT 1 Done')")
    sub_stage.add_argument("--comment", type=str, help="Optional AI note to attach to task")
    sub_stage.set_defaults(func=cmd_set_stage)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
