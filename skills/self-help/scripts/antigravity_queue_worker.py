#!/usr/bin/env python3
"""
Antigravity Autonomous Queue Worker v2.0
=======================================
Fully automated delegation bridge between the 24/7 Raspberry Pi Telegram Bot
(@SamanAssist96_bot) and PC Antigravity.

Modes:
  --check    : Returns JSON for Antigravity SessionStart / PreInvocation lifecycle hook.
  --process  : Autonomously executes all pending tasks immediately (music, reels, study).
  --watch    : Runs as a continuous background daemon checking queue every 10 seconds.
  --status   : Displays current queue health and tasks table.
  --add      : Enqueues a new task manually.
  --complete : Marks a task complete by ID.
"""

import os
import sys
import re
import json
import time
import fcntl
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
QUEUE_PATH = os.path.expanduser("~/Documents/OBSIDIAN/.antigravity_tasks_queue.json")
FALLBACK_QUEUE_PATH = "/mnt/saman-data/OBSIDIAN/.antigravity_tasks_queue.json"
MUSIC_DIR = os.path.expanduser("~/Music")
PLAYLISTS_DIR = os.path.join(MUSIC_DIR, "Playlists")
NODE_BIN = "/home/saman/.local/bin/node"

# Playlist & Mood Mappings
PLAYLIST_ALIASES = {
    "love": "Love ❤️.m3u",
    "war work": "⚔️ War-Work.m3u",
    "war-work": "⚔️ War-Work.m3u",
    "warwork": "⚔️ War-Work.m3u",
    "war": "⚔️ War-Work.m3u",
    "focus": "🎯 Focus.m3u",
    "study": "🎯 Focus.m3u",
    "chill": "🍃 Chill.m3u",
    "relax": "🍃 Chill.m3u",
    "sleep": "😴 Sleep.m3u",
    "sleeping": "😴 Sleep.m3u",
    "workout": "⚡ Adrenaline-Workout.m3u",
    "gym": "⚡ Adrenaline-Workout.m3u",
    "adrenaline": "⚡ Adrenaline-Workout.m3u",
    "devotion": "🙏 Devotion.m3u",
    "bhakti": "🙏 Devotion.m3u",
    "puja": "🙏 Devotion.m3u",
    "dugga": "🙏 Devotion.m3u",
    "shiva": "🙏 Devotion.m3u",
    "bgm": "🎼 BGM.m3u",
    "phonk": "🎼 BGM.m3u",
    "uplifting": "🌤️ Uplifting.m3u",
    "dopamine": "🌤️ Uplifting.m3u",
    "nostalgia": "📼 Nostalgia.m3u",
    "travel": "✈️ Travel.m3u",
    "trip": "✈️ Travel.m3u",
    "swadesh": "🇮🇳 Sdadesh- স্বদেশ.m3u",
    "desh": "🇮🇳 Sdadesh- স্বদেশ.m3u",
    "party": "🥳 Party.m3u",
    "sad": "🥀 Sad.m3u",
    "toxic": "☠️ Toxic.m3u",
    "jazz": "🎷 Jazz & Blues.m3u",
    "ghazal": "🌙 Ghazal & Classical.m3u",
    "prog rock": "🌀 Prog & Alt Rock.m3u",
    "rock": "🌀 Prog & Alt Rock.m3u",
    "grind": "🧠 Discipline - Grind.m3u",
    "discipline": "🧠 Discipline - Grind.m3u",
    "morning": "Morning 🌄.m3u",
    "numb": "Numb. 🩶.m3u",
    "sexy": "🔥 Sexy Mood.m3u",
    "self obsession": "👑 Self Obsession.m3u",
}

PLAYLIST_GENRES = {
    "Love ❤️.m3u": "Romance",
    "⚔️ War-Work.m3u": "Driving / Epic / Motivation",
    "🎯 Focus.m3u": "Intense Study / Focus",
    "🍃 Chill.m3u": "Soothing / Calm",
    "😴 Sleep.m3u": "Soothing / Calm",
    "⚡ Adrenaline-Workout.m3u": "Driving / Epic / Motivation",
    "🙏 Devotion.m3u": "Spiritual / Devotion",
    "🎼 BGM.m3u": "Chillstep / Deep Focus / Hustle",
    "🌤️ Uplifting.m3u": "Uplifting",
    "📼 Nostalgia.m3u": "Nostalgic",
    "✈️ Travel.m3u": "Driving",
    "🇮🇳 Sdadesh- স্বদেশ.m3u": "Patriotic / Swadesh / Bollywood Soundtrack",
    "🥳 Party.m3u": "Party",
    "🥀 Sad.m3u": "Sad / Emotional",
    "☠️ Toxic.m3u": "Dark / Seductive",
    "🎷 Jazz & Blues.m3u": "Jazz / Blues",
    "🌙 Ghazal & Classical.m3u": "Ghazal / Semi-classical",
    "🌀 Prog & Alt Rock.m3u": "Progressive / Art Rock",
    "🧠 Discipline - Grind.m3u": "Epic / Motivation",
    "Morning 🌄.m3u": "Soothing / Calm",
    "Numb. 🩶.m3u": "Soothing / Calm;Sad / Emotional",
    "🔥 Sexy Mood.m3u": "Dark / Seductive",
    "👑 Self Obsession.m3u": "Dark / Seductive"
}

def get_queue_file():
    if os.path.exists(QUEUE_PATH):
        return QUEUE_PATH
    if os.path.exists(FALLBACK_QUEUE_PATH):
        return FALLBACK_QUEUE_PATH
    return QUEUE_PATH

def load_queue():
    qfile = get_queue_file()
    if not os.path.exists(qfile):
        return {"queue_version": "1.0", "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tasks": []}
    try:
        with open(qfile, "r", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                data = json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
            return data
    except Exception as e:
        print(f"[QUEUE LOAD ERROR] {e}", file=sys.stderr)
        return {"queue_version": "1.0", "tasks": []}

def save_queue(data):
    qfile = get_queue_file()
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(qfile), exist_ok=True)
    temp_file = qfile + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    os.replace(temp_file, qfile)

def get_pending_tasks():
    data = load_queue()
    return [t for t in data.get("tasks", []) if t.get("status") == "pending"]

def add_task(url, task_type="add_music_playlist", user_id=571568364, raw_text=""):
    data = load_queue()
    task_id = f"task_{int(time.time())}"
    new_task = {
        "id": task_id,
        "user_id": user_id,
        "type": task_type,
        "url": url,
        "raw_text": raw_text or url,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
        "result": None
    }
    data.setdefault("tasks", []).append(new_task)
    save_queue(data)
    return new_task

def mark_task_complete(task_id, result=None, status="completed"):
    data = load_queue()
    for t in data.get("tasks", []):
        if t.get("id") == task_id:
            t["status"] = status
            t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t["result"] = result or {}
            break
    save_queue(data)

def send_telegram_alert(msg):
    """Sends notification to Saman via tg-bot-send."""
    try:
        cmd = ["tg-bot-send", "--message", msg]
        subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except Exception as e:
        print(f"[TG ALERT ERROR] {e}", file=sys.stderr)

def clean_title_and_artist(raw_title, uploader):
    cleaned = re.sub(r"[\(\[\{](?:official|audio|video|lyrics?|visualizer|hd|4k|remix|feat\.?|ft\.?).*?[\)\]\}]", "", raw_title, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    artist = uploader
    title = cleaned
    if "|" in cleaned:
        parts = [p.strip() for p in cleaned.split("|") if p.strip()]
        title = parts[0]
        artist = parts[1] if len(parts) > 1 else uploader
    elif " - " in cleaned:
        parts = cleaned.split(" - ", 1)
        artist = parts[0].strip()
        title = parts[1].strip()
    artist = re.sub(r"\s*(?:a\s+)?hoopr\s+original.*", "", artist, flags=re.IGNORECASE).strip()
    artist = re.sub(r"[\\/*?:\"<>|]", "", artist).strip() or "Unknown Artist"
    title = re.sub(r"[\\/*?:\"<>|]", "", title).strip() or "Unknown Title"
    return artist, title

def resolve_playlist(raw_text, title=""):
    text = f"{raw_text} {title}".lower()
    for key, filename in PLAYLIST_ALIASES.items():
        pattern = r"\b" + re.escape(key) + r"\b"
        if re.search(pattern, text):
            return os.path.join(PLAYLISTS_DIR, filename), filename
    # default fallback to Chill
    return os.path.join(PLAYLISTS_DIR, "🍃 Chill.m3u"), "🍃 Chill.m3u"

def process_music_task(task):
    """Autonomous downloader, tagger, cover extractor, and playlist appender."""
    url = task.get("url")
    raw_text = task.get("raw_text", "")
    task_id = task.get("id")
    print(f"[{datetime.now()}] [MUSIC WORKER] Processing {url}...")

    # 1. Fetch metadata with yt-dlp
    meta_cmd = [
        "yt-dlp",
        "--js-runtimes", f"node:{NODE_BIN}",
        "--dump-single-json",
        "--no-playlist",
        url
    ]
    meta_proc = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=30)
    if meta_proc.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata failed: {meta_proc.stderr}")

    meta = json.loads(meta_proc.stdout)
    raw_title = meta.get("title", "Unknown Title")
    uploader = meta.get("uploader") or meta.get("channel") or "Unknown Artist"
    duration = meta.get("duration_string", "Unknown Duration")

    artist, title = clean_title_and_artist(raw_title, uploader)
    album = f"{title} - Single"

    # Resolve target playlist
    playlist_path, playlist_name = resolve_playlist(raw_text, raw_title)
    genre = PLAYLIST_GENRES.get(playlist_name, "Soothing / Calm")

    # Directory layout: ~/Music/<Artist>/<Album or Single>/
    dest_dir = os.path.join(MUSIC_DIR, artist, album)
    os.makedirs(dest_dir, exist_ok=True)
    audio_path = os.path.join(dest_dir, f"{artist} - {title}.m4a")
    cover_path = os.path.join(dest_dir, "cover.jpg")

    # 2. Download audio if not exists
    if not os.path.exists(audio_path):
        dl_cmd = [
            "yt-dlp",
            "--js-runtimes", f"node:{NODE_BIN}",
            "-x", "--audio-format", "m4a", "--audio-quality", "0",
            "--embed-thumbnail",
            "-o", os.path.join(dest_dir, f"{artist} - {title}.%(ext)s"),
            url
        ]
        dl_proc = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=120)
        if dl_proc.returncode != 0:
            raise RuntimeError(f"yt-dlp download failed: {dl_proc.stderr}")

    # 3. Extract cover.jpg if not exists
    if not os.path.exists(cover_path) and os.path.exists(audio_path):
        try:
            cov_cmd = ["ffmpeg", "-y", "-i", audio_path, "-map", "0:v", "-frames:v", "1", cover_path]
            subprocess.run(cov_cmd, capture_output=True, text=True, timeout=15)
        except Exception as e:
            print(f"[COVER EXTRACT WARN] {e}", file=sys.stderr)

    # 4. Tag with mutagen
    try:
        from mutagen.mp4 import MP4
        audio = MP4(audio_path)
        audio["\xa9nam"] = [title]
        audio["\xa9ART"] = [artist]
        audio["\xa9alb"] = [album]
        audio["\xa9gen"] = [genre]
        audio["\xa9cmt"] = [url]
        audio.save()
    except Exception as e:
        print(f"[MUTAGEN WARN] {e}", file=sys.stderr)

    # 5. Append to target .m3u playlist (relative path)
    rel_path = f"../{artist}/{album}/{artist} - {title}.m4a"
    if os.path.exists(playlist_path):
        with open(playlist_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        if rel_path not in lines:
            with open(playlist_path, "a", encoding="utf-8") as f:
                f.write(f"{rel_path}\n")
    else:
        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write(f"#EXTM3U\n{rel_path}\n")

    result = {
        "title": title,
        "artist": artist,
        "album": album,
        "playlist": playlist_name,
        "duration": duration,
        "file_path": audio_path
    }
    mark_task_complete(task_id, result=result, status="completed")

    # 6. Notify Telegram
    alert_msg = (
        f"🎵 <b>স্বয়ংক্রিয় মিউজিক ডাউনলোড সম্পন্ন!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎶 <b>গান:</b> {title}\n"
        f"👤 <b>শিল্পী:</b> {artist}\n"
        f"⏱️ <b>দৈর্ঘ্য:</b> {duration}\n"
        f"📂 <b>প্লেলিস্ট:</b> <code>{playlist_name}</code>\n"
        f"💾 <b>লোকেশন:</b> <code>{artist}/{album}/</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Antigravity অটোনোমাস ইঞ্জিন আপনার অনুরোধ সফলভাবে সম্পন্ন করেছে এবং লাইব্রেরি সিঙ্ক করা হয়েছে!</i>"
    )
    send_telegram_alert(alert_msg)
    print(f"[{datetime.now()}] [MUSIC WORKER] Done: {title} -> {playlist_name}")
    return result

def process_self_help_task(task):
    """Processes self-help reels and logs protocols to Obsidian."""
    url = task.get("url")
    task_id = task.get("id")
    print(f"[{datetime.now()}] [SELF-HELP WORKER] Processing {url}...")

    # For reels, extract metadata/description
    meta_cmd = [
        "yt-dlp",
        "--dump-single-json",
        "--no-playlist",
        url
    ]
    meta_proc = subprocess.run(meta_cmd, capture_output=True, text=True, timeout=45)
    title = "Self Help Protocol"
    desc = ""
    if meta_proc.returncode == 0:
        meta = json.loads(meta_proc.stdout)
        title = meta.get("title") or "Self Help Exercise / Protocol"
        desc = meta.get("description", "")

    note_name = re.sub(r"[\\/*?:\"<>|]", "", title)[:50].strip() or f"Protocol_{int(time.time())}"
    note_dir = os.path.expanduser("~/Documents/OBSIDIAN/SELF HELP/Protocols")
    os.makedirs(note_dir, exist_ok=True)
    note_path = os.path.join(note_dir, f"{note_name}.md")

    with open(note_path, "w", encoding="utf-8") as f:
        f.write(f"# 🧠 {title}\n\n")
        f.write(f"> **Source:** [{url}]({url})\n")
        f.write(f"> **Captured At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## 📝 Overview & Notes\n\n{desc}\n")

    result = {
        "title": title,
        "obsidian_note": note_path
    }
    mark_task_complete(task_id, result=result, status="completed")

    alert_msg = (
        f"🧠 <b>সেলফ-হেল্প প্রটোকল বিশ্লেষণ সম্পন্ন!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>শিরোনাম:</b> {title}\n"
        f"📂 <b>Obsidian নোট:</b> <code>Protocols/{note_name}.md</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <i>Antigravity অটোনোমাস ইঞ্জিন আপনার রিলটি বিশ্লেষণ করে নোটে সেভ করেছে!</i>"
    )
    send_telegram_alert(alert_msg)
    print(f"[{datetime.now()}] [SELF-HELP WORKER] Done: {title}")
    return result

def process_all_pending():
    """Iterates through all pending tasks and executes them autonomously."""
    pending = get_pending_tasks()
    if not pending:
        print(f"[{datetime.now()}] Queue clean: 0 pending tasks.")
        return 0

    print(f"[{datetime.now()}] Found {len(pending)} pending task(s). Starting autonomous execution...")
    processed = 0
    for t in pending:
        task_id = t.get("id")
        task_type = t.get("type")
        url = t.get("url")
        try:
            if task_type == "add_music_playlist":
                process_music_task(t)
            elif task_type in ("extract_self_help_reel", "self_help"):
                process_self_help_task(t)
            elif task_type == "test_task":
                mark_task_complete(task_id, result={"msg": "test completed"})
            else:
                # Default to music if youtube link
                if "youtube.com" in url or "youtu.be" in url:
                    process_music_task(t)
                else:
                    process_self_help_task(t)
            processed += 1
        except Exception as e:
            print(f"[{datetime.now()}] [TASK ERROR] Task {task_id} failed: {e}", file=sys.stderr)
            mark_task_complete(task_id, result={"error": str(e)}, status="failed")
            send_telegram_alert(f"⚠️ <b>টাস্ক এক্সিকিউশন ত্রুটি!</b>\nটাস্ক আইডি: <code>{task_id}</code>\nত্রুটি: <code>{str(e)[:300]}</code>")

    return processed

def check_for_hook():
    """Hook contract for Antigravity SessionStart/PreInvocation."""
    pending = get_pending_tasks()
    if not pending:
        print("{}")
        return

    task_summaries = []
    for i, t in enumerate(pending, 1):
        raw = f" | Request: {t.get('raw_text')}" if t.get("raw_text") else ""
        task_summaries.append(f"{i}. [ID: {t['id']}] Type: {t.get('type')} | URL: {t.get('url')} (Queued at {t.get('created_at')}){raw}")

    inject_msg = (
        "🔔 [TELEGRAM BOT DELEGATED TASKS DETECTED IN QUEUE]\n"
        "The homeserver Telegram bot (@SamanAssist96_bot) queued the following pending task(s) for Antigravity:\n"
        + "\n".join(task_summaries)
        + "\n\n⚡ INSTRUCTION: Immediately execute these pending tasks without waiting for manual user prompting:\n"
        "• For 'add_music_playlist': download high-quality audio via yt-dlp to /home/saman/Music/Artist/Album/, extract cover.jpg, tag with mutagen (title, artist, album, genre), append relative path to target .m3u playlist in /home/saman/Music/Playlists/, mark task completed in queue via `antigravity_queue_worker.py --complete <ID>`, and send confirmation via `tg-bot-send`.\n"
        "• For 'extract_self_help_reel': analyze video/audio with yt-dlp/Gemini, update /self-help CLI/skill and Obsidian notes, mark task completed, and send confirmation via `tg-bot-send`."
    )

    hook_output = {
        "injectSteps": [
            {
                "systemMessage": {
                    "systemMessage": inject_msg
                }
            }
        ]
    }
    print(json.dumps(hook_output))

def watch_loop(poll_interval=10):
    """Continuous polling daemon mode."""
    print(f"[{datetime.now()}] Antigravity Autonomous Queue Watcher started. Polling every {poll_interval}s...")
    while True:
        try:
            process_all_pending()
        except Exception as e:
            print(f"[{datetime.now()}] [WATCHER LOOP ERROR] {e}", file=sys.stderr)
        time.sleep(poll_interval)

def list_status():
    data = load_queue()
    tasks = data.get("tasks", [])
    print(f"\n--- Antigravity Delegation Queue ({len(tasks)} tasks total) ---")
    print(f"Queue File: {get_queue_file()}")
    print(f"{'ID':<24} | {'Status':<10} | {'Type':<24} | {'URL / Description'}")
    print("-" * 80)
    for t in tasks:
        print(f"{t.get('id', ''):<24} | {t.get('status', ''):<10} | {t.get('type', ''):<24} | {t.get('url', '')}")
    print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Autonomous Queue Worker")
    parser.add_argument("--check", action="store_true", help="Hook mode for SessionStart/PreInvocation")
    parser.add_argument("--process", action="store_true", help="Process all pending tasks immediately")
    parser.add_argument("--watch", action="store_true", help="Run as continuous background watcher")
    parser.add_argument("--status", action="store_true", help="List all tasks in queue")
    parser.add_argument("--add", help="Add a URL to the queue")
    parser.add_argument("--type", default="add_music_playlist", help="Task type")
    parser.add_argument("--text", default="", help="Raw request text / user prompt")
    parser.add_argument("--complete", help="Mark task ID as complete")
    args = parser.parse_args()

    if args.check:
        check_for_hook()
    elif args.process:
        process_all_pending()
    elif args.watch:
        watch_loop()
    elif args.status:
        list_status()
    elif args.add:
        t = add_task(args.add, task_type=args.type, raw_text=args.text)
        print(f"Added task {t['id']} to queue.")
    elif args.complete:
        mark_task_complete(args.complete)
        print(f"Marked task {args.complete} as complete.")
    else:
        list_status()

if __name__ == "__main__":
    main()
