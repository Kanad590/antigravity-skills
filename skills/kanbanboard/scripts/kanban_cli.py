#!/usr/bin/env python3
"""
Kanbanboard CLI Client for Antigravity & User Management
Interface for Kanboard JSON-RPC 2.0 API with auto-routing (LAN/Tailscale).
"""
import sys
import os
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime
import argparse

LAN_URL = "http://192.168.1.100:1337/jsonrpc.php"
TS_URL = "http://100.x.y.z:1337/jsonrpc.php"
USER = "ai"
TOKEN = "YOUR_KANBOARD_API_TOKEN"
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{TOKEN}".encode("utf-8")).decode("utf-8")

def get_rpc_url():
    """Try LAN first (1s timeout), fall back to Tailscale."""
    for url in [LAN_URL, TS_URL]:
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps({"jsonrpc": "2.0", "method": "getVersion", "id": 1}).encode("utf-8"),
                headers={"Content-Type": "application/json", "Authorization": AUTH_HEADER}
            )
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    return url
        except Exception:
            continue
    return LAN_URL

def call_rpc(method, params=None, url=None):
    if not url:
        url = get_rpc_url()
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": params or {}
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": AUTH_HEADER}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "error" in data:
                print(f"❌ Kanboard API Error: {data['error']}", file=sys.stderr)
                sys.exit(1)
            return data.get("result")
    except urllib.error.URLError as e:
        print(f"❌ Network connection failed to {url}: {e}", file=sys.stderr)
        sys.exit(1)

# ==========================================
# Commands
# ==========================================

def cmd_summary(args):
    """Print high-level dashboard of both active projects."""
    print("=" * 70)
    print("             📋 KANBOARD OVERVIEW & STATUS SUMMARY")
    print("=" * 70)
    projects = call_rpc("getAllProjects")
    active_projects = [p for p in projects if p.get("is_active") == 1]
    
    for p in active_projects:
        pid = p["id"]
        pname = p["name"]
        cols = call_rpc("getColumns", {"project_id": pid})
        tasks = call_rpc("getAllTasks", {"project_id": pid, "status_id": 1})
        col_map = {c["id"]: c["title"] for c in cols}
        counts = {c["title"]: 0 for c in cols}
        for t in tasks:
            col_title = col_map.get(t["column_id"], f"Col {t['column_id']}")
            counts[col_title] = counts.get(col_title, 0) + 1
            
        print(f"\n📂 Project #{pid}: {pname}")
        print(f"   Total Active Tasks: {len(tasks)}")
        print("   Column Distribution:")
        for ctitle, count in counts.items():
            if count > 0:
                print(f"     • {ctitle:<38} : {count:>3} tasks")
    print("=" * 70)

def cmd_projects(args):
    """List all projects."""
    projects = call_rpc("getAllProjects")
    print(f"{'ID':<4} {'Status':<10} {'Name'}")
    print("-" * 60)
    for p in projects:
        status = "Active" if p.get("is_active") == 1 else "Archived"
        print(f"{p['id']:<4} {status:<10} {p['name']}")

def cmd_columns(args):
    """List columns for a project."""
    cols = call_rpc("getColumns", {"project_id": args.project_id})
    print(f"Columns for Project #{args.project_id}:")
    print(f"{'ID':<6} {'Pos':<4} {'Limit':<6} {'Title'}")
    print("-" * 50)
    for c in cols:
        print(f"{c['id']:<6} {c['position']:<4} {c['task_limit']:<6} {c['title']}")

def cmd_categories(args):
    """List categories for a project."""
    cats = call_rpc("getAllCategories", {"project_id": args.project_id})
    print(f"Categories for Project #{args.project_id}:")
    print(f"{'ID':<6} {'Name'}")
    print("-" * 40)
    for c in cats:
        print(f"{c['id']:<6} {c['name']}")

def cmd_tags(args):
    """List tags for a project."""
    tags = call_rpc("getTagsByProject", {"project_id": args.project_id})
    print(f"Tags for Project #{args.project_id}:")
    for t in tags:
        print(f"  • {t['name']} (ID: {t['id']})")

def cmd_tasks(args):
    """List tasks in a project with filtering."""
    query_parts = []
    if args.status == "open":
        query_parts.append("status:open")
    elif args.status == "closed":
        query_parts.append("status:closed")
    
    if args.column:
        query_parts.append(f"column:\"{args.column}\"")
    if args.category:
        query_parts.append(f"category:\"{args.category}\"")
    if args.search:
        query_parts.append(args.search)
        
    query = " ".join(query_parts) if query_parts else "status:open"
    tasks = call_rpc("searchTasks", {"project_id": args.project_id, "query": query})
    
    print(f"Found {len(tasks)} tasks matching query: [{query}]")
    print(f"{'ID':<6} {'Column':<24} {'Title'}")
    print("-" * 80)
    for t in tasks:
        col = t.get("column_name", f"Col {t.get('column_id')}")[:22]
        title = t.get("title", "")[:50]
        print(f"#{t['id']:<5} {col:<24} {title}")

def cmd_task(args):
    """Show detailed view of a single task."""
    task = call_rpc("getTask", {"task_id": args.task_id})
    if not task:
        print(f"Task #{args.task_id} not found.")
        return
        
    print("=" * 70)
    print(f"Task #{task['id']}: {task['title']}")
    print("=" * 70)
    print(f"• Project ID: {task['project_id']} | Column ID: {task['column_id']}")
    print(f"• Priority: {task['priority']} | Color: {task.get('color_id')}")
    print(f"• Created: {datetime.fromtimestamp(int(task['date_creation'])).strftime('%Y-%m-%d %H:%M') if task.get('date_creation') else 'N/A'}")
    if task.get('date_due') and int(task['date_due']) > 0:
        print(f"• Due Date: {datetime.fromtimestamp(int(task['date_due'])).strftime('%Y-%m-%d %H:%M')}")
    
    tags = call_rpc("getTaskTags", {"task_id": args.task_id})
    if tags:
        print(f"• Tags: {', '.join(tags.values())}")
        
    subtasks = call_rpc("getAllSubtasks", {"task_id": args.task_id})
    if subtasks:
        print(f"\n▶ Subtasks ({len(subtasks)}):")
        for s in subtasks:
            status_symbol = "✅" if s["status"] == 2 else ("⏳" if s["status"] == 1 else "⬜")
            print(f"  {status_symbol} #{s['id']}: {s['title']}")
            
    comments = call_rpc("getAllComments", {"task_id": args.task_id})
    if comments:
        print(f"\n▶ Comments ({len(comments)}):")
        for c in comments:
            dt = datetime.fromtimestamp(int(c.get("date_creation", 0))).strftime('%Y-%m-%d %H:%M') if c.get("date_creation") else ""
            print(f"  💬 [User #{c['user_id']} @ {dt}]:")
            for line in c["comment"].splitlines()[:6]:
                print(f"     {line}")
                
    if task.get("description"):
        print(f"\n▶ Description:")
        for line in task["description"].splitlines()[:15]:
            print(f"  {line}")
        if len(task["description"].splitlines()) > 15:
            print("  ... [truncated, run with full view to see entire description]")
    print("=" * 70)

def cmd_create(args):
    """Create a new task."""
    params = {
        "title": args.title,
        "project_id": args.project_id,
        "owner_id": 2, # AI user
    }
    if args.column_id:
        params["column_id"] = args.column_id
    if args.description:
        params["description"] = args.description
    if args.priority is not None:
        params["priority"] = args.priority
    if args.due:
        dt = datetime.strptime(args.due, "%Y-%m-%d")
        params["date_due"] = int(dt.timestamp())
    if args.tags:
        params["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
        
    task_id = call_rpc("createTask", params)
    print(f"✅ Created Task #{task_id} in Project #{args.project_id}: '{args.title}'")

def cmd_move(args):
    """Move task to a column."""
    task = call_rpc("getTask", {"task_id": args.task_id})
    if not task:
        print(f"Task #{args.task_id} not found.")
        return
        
    project_id = task["project_id"]
    cols = call_rpc("getColumns", {"project_id": project_id})
    
    target_col_id = None
    target_col_title = ""
    # Try ID match first
    for c in cols:
        if str(c["id"]) == str(args.column) or c["title"].lower().strip() == args.column.lower().strip() or args.column.lower().strip() in c["title"].lower():
            target_col_id = c["id"]
            target_col_title = c["title"]
            break
            
    if not target_col_id:
        print(f"❌ Error: Column '{args.column}' not found in Project #{project_id}.", file=sys.stderr)
        print("Available columns:")
        for c in cols:
            print(f"  • {c['id']}: {c['title']}")
        sys.exit(1)
        
    res = call_rpc("moveTaskPosition", {
        "project_id": project_id,
        "task_id": args.task_id,
        "column_id": target_col_id,
        "position": 1,
        "swimlane_id": task.get("swimlane_id", 0)
    })
    if res:
        print(f"✅ Successfully moved Task #{args.task_id} ('{task['title']}') -> '{target_col_title}'")
    else:
        print(f"❌ Failed to move task #{args.task_id}")

def cmd_comment(args):
    """Add a comment to a task as AI user #2."""
    comment_id = call_rpc("createComment", {
        "task_id": args.task_id,
        "user_id": 2,
        "content": args.content
    })
    print(f"✅ Added Comment #{comment_id} to Task #{args.task_id}")

def cmd_close(args):
    """Close a task."""
    res = call_rpc("closeTask", {"task_id": args.task_id})
    print(f"✅ Task #{args.task_id} closed." if res else f"❌ Failed to close Task #{args.task_id}")

def cmd_open(args):
    """Reopen a task."""
    res = call_rpc("openTask", {"task_id": args.task_id})
    print(f"✅ Task #{args.task_id} reopened." if res else f"❌ Failed to reopen Task #{args.task_id}")

def cmd_subtask_add(args):
    """Add a subtask."""
    subtask_id = call_rpc("createSubtask", {
        "task_id": args.task_id,
        "title": args.title,
        "status": 0
    })
    print(f"✅ Created Subtask #{subtask_id} for Task #{args.task_id}: '{args.title}'")

def cmd_subtask_toggle(args):
    """Toggle a subtask status (0=todo -> 1=in progress -> 2=done -> 0=todo)."""
    subtask = call_rpc("getSubtask", {"subtask_id": args.subtask_id})
    if not subtask:
        print(f"Subtask #{args.subtask_id} not found.")
        return
    current_status = subtask["status"]
    next_status = (current_status + 1) % 3
    status_names = {0: "TODO (⬜)", 1: "IN PROGRESS (⏳)", 2: "DONE (✅)"}
    call_rpc("updateSubtask", {
        "id": args.subtask_id,
        "task_id": subtask["task_id"],
        "status": next_status
    })
    print(f"✅ Subtask #{args.subtask_id} updated: {status_names[current_status]} ➔ {status_names[next_status]}")

def cmd_tag_add(args):
    """Add a tag to a task."""
    tags = call_rpc("getTaskTags", {"task_id": args.task_id}) or {}
    current_tags = list(tags.values())
    if args.tag not in current_tags:
        current_tags.append(args.tag)
        task = call_rpc("getTask", {"task_id": args.task_id})
        call_rpc("setTaskTags", {"project_id": task["project_id"], "task_id": args.task_id, "tags": current_tags})
        print(f"✅ Added tag '{args.tag}' to Task #{args.task_id}. Current tags: {', '.join(current_tags)}")
    else:
        print(f"Tag '{args.tag}' is already present on Task #{args.task_id}.")

def main():
    parser = argparse.ArgumentParser(description="Kanboard CLI for Antigravity & User")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    # summary
    sub_summary = subparsers.add_parser("summary", help="Show overview of active projects & boards")
    sub_summary.set_defaults(func=cmd_summary)
    
    # projects
    sub_proj = subparsers.add_parser("projects", help="List all projects")
    sub_proj.set_defaults(func=cmd_projects)
    
    # columns
    sub_col = subparsers.add_parser("columns", help="List columns for a project")
    sub_col.add_argument("project_id", type=int, help="Project ID")
    sub_col.set_defaults(func=cmd_columns)
    
    # categories
    sub_cat = subparsers.add_parser("categories", help="List categories for a project")
    sub_cat.add_argument("project_id", type=int, help="Project ID")
    sub_cat.set_defaults(func=cmd_categories)
    
    # tags
    sub_tag = subparsers.add_parser("tags", help="List tags for a project")
    sub_tag.add_argument("project_id", type=int, help="Project ID")
    sub_tag.set_defaults(func=cmd_tags)
    
    # tasks
    sub_tasks = subparsers.add_parser("tasks", help="List tasks in a project")
    sub_tasks.add_argument("project_id", type=int, help="Project ID")
    sub_tasks.add_argument("--column", type=str, help="Filter by column title")
    sub_tasks.add_argument("--category", type=str, help="Filter by category")
    sub_tasks.add_argument("--status", choices=["open", "closed", "all"], default="open", help="Filter by status")
    sub_tasks.add_argument("--search", type=str, help="Search query string")
    sub_tasks.set_defaults(func=cmd_tasks)
    
    # task
    sub_task = subparsers.add_parser("task", help="View full task details")
    sub_task.add_argument("task_id", type=int, help="Task ID")
    sub_task.set_defaults(func=cmd_task)
    
    # create
    sub_create = subparsers.add_parser("create", help="Create a new task")
    sub_create.add_argument("project_id", type=int, help="Project ID")
    sub_create.add_argument("title", type=str, help="Task title")
    sub_create.add_argument("--column-id", type=int, help="Target column ID")
    sub_create.add_argument("--description", type=str, help="Task description")
    sub_create.add_argument("--priority", type=int, default=0, help="Priority (0-3)")
    sub_create.add_argument("--due", type=str, help="Due date YYYY-MM-DD")
    sub_create.add_argument("--tags", type=str, help="Comma-separated tags")
    sub_create.set_defaults(func=cmd_create)
    
    # move
    sub_move = subparsers.add_parser("move", help="Move a task to another column")
    sub_move.add_argument("task_id", type=int, help="Task ID")
    sub_move.add_argument("column", type=str, help="Target column title or ID")
    sub_move.set_defaults(func=cmd_move)
    
    # close / open
    sub_close = subparsers.add_parser("close", help="Close a task")
    sub_close.add_argument("task_id", type=int, help="Task ID")
    sub_close.set_defaults(func=cmd_close)
    
    sub_open = subparsers.add_parser("open", help="Reopen a task")
    sub_open.add_argument("task_id", type=int, help="Task ID")
    sub_open.set_defaults(func=cmd_open)
    
    # comment
    sub_comment = subparsers.add_parser("comment", help="Add a comment to a task")
    sub_comment.add_argument("task_id", type=int, help="Task ID")
    sub_comment.add_argument("content", type=str, help="Comment content")
    sub_comment.set_defaults(func=cmd_comment)
    
    # subtask-add
    sub_sadd = subparsers.add_parser("subtask-add", help="Add a subtask to a task")
    sub_sadd.add_argument("task_id", type=int, help="Task ID")
    sub_sadd.add_argument("title", type=str, help="Subtask title")
    sub_sadd.set_defaults(func=cmd_subtask_add)
    
    # subtask-toggle
    sub_stoggle = subparsers.add_parser("subtask-toggle", help="Toggle a subtask status")
    sub_stoggle.add_argument("subtask_id", type=int, help="Subtask ID")
    sub_stoggle.set_defaults(func=cmd_subtask_toggle)
    
    # tag-add
    sub_tadd = subparsers.add_parser("tag-add", help="Add a tag to a task")
    sub_tadd.add_argument("task_id", type=int, help="Task ID")
    sub_tadd.add_argument("tag", type=str, help="Tag name")
    sub_tadd.set_defaults(func=cmd_tag_add)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
