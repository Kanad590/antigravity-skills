#!/usr/bin/env python3
"""
Exam Quiz & Active Recall Flashcard Generator
Extracts study material from PDFs (e.g. Master Study Note, Zotero PYQs, Obsidian notes),
formats active recall flashcards, and can dispatch daily questions to Telegram.
"""

import sys
import os
import argparse
import json
import subprocess

try:
    import pymupdf as fitz
except ImportError:
    import fitz

OBSIDIAN_VAULT = os.path.expanduser('~/Documents/OBSIDIAN')
FLASHCARDS_DIR = os.path.join(OBSIDIAN_VAULT, 'Flashcards')

def extract_pdf_text(pdf_path, start_page=1, end_page=None, max_chars=4000):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    start_idx = max(0, start_page - 1)
    end_idx = min(total_pages, end_page) if end_page else total_pages

    extracted = []
    total_len = 0
    for page_num in range(start_idx, end_idx):
        text = doc[page_num].get_text()
        extracted.append(f"--- [Page {page_num + 1}] ---\n{text}")
        total_len += len(text)
        if total_len >= max_chars:
            break
            
    doc.close()
    return "\n".join(extracted)

def send_telegram_quiz(question_text, topic="Exam Prep"):
    cmd = ["tg-bot-send", "--message", f"🎯 *Quiz: {topic}*\n\n{question_text}"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("Successfully sent quiz to Telegram.")
        return True
    else:
        # Fallback to python backend
        py_backend = os.path.expanduser("~/.config/telegram-sender/bot_send.py")
        if os.path.exists(py_backend):
            r = subprocess.run(["python3", py_backend, "-m", f"🎯 *Quiz: {topic}*\n\n{question_text}"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return r.returncode == 0
        print(f"Failed to send to Telegram: {res.stderr}", file=sys.stderr)
        return False

def save_to_obsidian_flashcard(deck_name, q_and_a_markdown):
    os.makedirs(FLASHCARDS_DIR, exist_ok=True)
    filename = f"{deck_name.replace(' ', '_')}_Deck.md"
    target_path = os.path.join(FLASHCARDS_DIR, filename)
    with open(target_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n# Active Recall Deck: {deck_name}\n")
        f.write(q_and_a_markdown)
    print(f"Saved flashcards to {target_path}")
    return target_path

def main():
    parser = argparse.ArgumentParser(description="Exam Quiz & Flashcard Generator")
    subparsers = parser.add_subparsers(dest="command")

    # extract
    ext_p = subparsers.add_parser("extract", help="Extract text from a study PDF")
    ext_p.add_argument("pdf_path", help="Path to PDF")
    ext_p.add_argument("--start", type=int, default=1, help="Start page (1-based)")
    ext_p.add_argument("--end", type=int, default=5, help="End page (1-based)")
    ext_p.add_argument("--max-chars", type=int, default=5000, help="Max characters to extract")

    # send-quiz
    send_p = subparsers.add_parser("send-quiz", help="Send a quiz question to Telegram")
    send_p.add_argument("--topic", default="Daily Revision", help="Subject/Topic name")
    send_p.add_argument("--question", required=True, help="Question text (Markdown allowed)")

    # save-deck
    deck_p = subparsers.add_parser("save-deck", help="Append flashcards to Obsidian vault")
    deck_p.add_argument("--deck", default="Manufacturing_Science", help="Deck name")
    deck_p.add_argument("--content", required=True, help="Flashcard content in Markdown")

    args = parser.parse_args()

    if args.command == "extract":
        text = extract_pdf_text(args.pdf_path, args.start, args.end, args.max_chars)
        print(text)

    elif args.command == "send-quiz":
        send_telegram_quiz(args.question, args.topic)

    elif args.command == "save-deck":
        save_to_obsidian_flashcard(args.deck, args.content)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
