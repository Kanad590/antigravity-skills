#!/usr/bin/env python3
"""
Kanboard JSON-RPC 2.0 Client for Self-Help & Study Tracking
Supports dual-routing (LAN and Tailscale) with automatic failover,
connection caching, and resilient offline error handling.
"""
import sys
import os
import json
import base64
import urllib.request
import urllib.error

LAN_URL = "http://192.168.1.100:1337/jsonrpc.php"
TS_URL = "http://100.x.y.z:1337/jsonrpc.php"
USER = "ai"
TOKEN = "YOUR_KANBOARD_API_TOKEN"
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{TOKEN}".encode("utf-8")).decode("utf-8")

PROJECT_EXAMS = 4
PROJECT_SYLLABUS = 5

_CACHED_URL = None

def check_connection(url, timeout=1.5):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps({"jsonrpc": "2.0", "method": "getVersion", "id": 1}).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": AUTH_HEADER}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False

def get_rpc_url(force_refresh=False):
    global _CACHED_URL
    if _CACHED_URL and not force_refresh:
        return _CACHED_URL
    if check_connection(LAN_URL):
        _CACHED_URL = LAN_URL
        return LAN_URL
    if check_connection(TS_URL):
        _CACHED_URL = TS_URL
        return TS_URL
    _CACHED_URL = None
    return None

def call_rpc(method, params=None):
    global _CACHED_URL
    url = get_rpc_url()
    if not url:
        return {"error": "Homeserver Kanboard is currently unreachable on LAN and Tailscale."}
    
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
        with urllib.request.urlopen(req, timeout=6.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "error" in data:
                return {"error": str(data["error"])}
            return {"result": data.get("result")}
    except Exception as e:
        _CACHED_URL = None  # Invalidate cached URL on connection error
        return {"error": f"RPC Exception: {e}"}

def get_exam_tasks():
    res = call_rpc("getAllTasks", {"project_id": PROJECT_EXAMS, "status_id": 1})
    if "error" in res:
        return {"result": [], "error": res["error"]}
    return {"result": res.get("result") or []}

def get_syllabus_summary():
    res = call_rpc("getAllTasks", {"project_id": PROJECT_SYLLABUS, "status_id": 1})
    if "error" in res:
        return {"total": 0, "breakdown": {}, "error": res["error"]}
    tasks = res.get("result") or []
    cols_res = call_rpc("getColumns", {"project_id": PROJECT_SYLLABUS})
    cols = cols_res.get("result") or []
    col_map = {c["id"]: c["title"] for c in cols if isinstance(c, dict)}
    
    breakdown = {}
    for t in tasks:
        if isinstance(t, dict):
            col_name = col_map.get(t.get("column_id"), "Unknown")
            breakdown.setdefault(col_name, []).append(t.get("title"))
    return {"total": len(tasks), "breakdown": breakdown}

if __name__ == "__main__":
    url = get_rpc_url()
    if url:
        print(f"✅ Kanboard connected successfully via: {url}")
        res = call_rpc("getVersion")
        print(f"📌 Server Version: {res.get('result')}")
    else:
        print("⚠️ Kanboard server is unreachable (offline mode active).")
