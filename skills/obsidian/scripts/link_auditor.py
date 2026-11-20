#!/usr/bin/env python3
"""
Obsidian Vault Link & Attachment Auditor
Parses all Wikilinks [[...]] and Embeds ![[...]] across notes and canvases.
Identifies broken links, missing attachments, orphaned notes, and unused media.
Distinguishes native Obsidian .canvas files from media attachments.
"""
import sys
import os
import re
import json
import argparse
from collections import defaultdict

WIKILINK_RE = re.compile(r'(!?)\[\[([^\]\n]+)\]\]')

def clean_link_target(raw_target):
    # Handle alias or dimension: [[file|alias]] or ![[file|250]]
    target = raw_target.split('|')[0].strip()
    # Handle heading or block anchor: [[file#heading]] or [[#heading]]
    target = target.split('#')[0].strip()
    return target

def audit_vault(vault_dir, ignore_archive=True):
    all_notes = {}       # normalized base name -> full relative path
    all_canvases = {}    # canvas filename/relpath -> full relative path
    all_attachments = {} # media filename -> full relative path
    outlinks = defaultdict(set)
    inlinks = defaultdict(set)
    broken_links = defaultdict(list)
    broken_embeds = defaultdict(list)

    # 1. Index all files
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (ignore_archive and d.startswith('_Archive'))]
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, vault_dir)
            base_name, ext = os.path.splitext(file)
            ext = ext.lower()

            if ext == '.md':
                rel_no_ext = os.path.splitext(rel_path)[0]
                all_notes[base_name] = rel_path
                all_notes[file] = rel_path
                all_notes[rel_path] = rel_path
                all_notes[rel_no_ext] = rel_path
            elif ext == '.canvas':
                rel_no_ext = os.path.splitext(rel_path)[0]
                all_canvases[base_name] = rel_path
                all_canvases[file] = rel_path
                all_canvases[rel_path] = rel_path
                all_canvases[rel_no_ext] = rel_path
            else:
                rel_no_ext = os.path.splitext(rel_path)[0]
                all_attachments[file] = rel_path
                all_attachments[rel_path] = rel_path
                all_attachments[rel_no_ext] = rel_path

    # Helper to resolve link target
    def resolve_target(target):
        if target in all_notes:
            return all_notes[target]
        if target in all_canvases:
            return all_canvases[target]
        if target in all_attachments:
            return all_attachments[target]
        base = os.path.basename(target)
        if base in all_notes:
            return all_notes[base]
        if base in all_canvases:
            return all_canvases[base]
        if base in all_attachments:
            return all_attachments[base]
        return None

    # 2. Parse links in Markdown files
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (ignore_archive and d.startswith('_Archive'))]
        for file in files:
            if not file.endswith('.md'):
                continue
            full_path = os.path.join(root, file)
            src_rel = os.path.relpath(full_path, vault_dir)

            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            matches = WIKILINK_RE.findall(content)
            for is_embed, raw_target in matches:
                target = clean_link_target(raw_target)
                if not target:
                    continue

                dest = resolve_target(target)
                if dest:
                    outlinks[src_rel].add(dest)
                    inlinks[dest].add(src_rel)
                elif is_embed:
                    broken_embeds[src_rel].append(raw_target)
                else:
                    # Check cross-vault link to sibling vault
                    parent_vault = os.path.dirname(vault_dir)
                    if (os.path.exists(os.path.join(parent_vault, target)) or 
                        os.path.exists(os.path.join(parent_vault, target + '.md')) or
                        os.path.exists(os.path.join(parent_vault, target + '.canvas'))):
                        outlinks[src_rel].add(target)
                        inlinks[target].add(src_rel)
                    else:
                        broken_links[src_rel].append(raw_target)

    # 3. Parse Canvas files
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (ignore_archive and d.startswith('_Archive'))]
        for file in files:
            if not file.endswith('.canvas'):
                continue
            full_path = os.path.join(root, file)
            src_rel = os.path.relpath(full_path, vault_dir)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    canvas_data = json.load(f)
                for node in canvas_data.get('nodes', []):
                    if node.get('type') == 'file':
                        fpath = node.get('file', '')
                        dest = resolve_target(fpath)
                        if dest:
                            outlinks[src_rel].add(dest)
                            inlinks[dest].add(src_rel)
                        else:
                            broken_links[src_rel].append(fpath)
                    elif node.get('type') == 'text':
                        text = node.get('text', '')
                        for is_embed, raw_target in WIKILINK_RE.findall(text):
                            target = clean_link_target(raw_target)
                            if not target:
                                continue
                            dest = resolve_target(target)
                            if dest:
                                outlinks[src_rel].add(dest)
                                inlinks[dest].add(src_rel)
                            else:
                                broken_links[src_rel].append(raw_target)
            except Exception:
                pass

    # 4. Orphans and unused
    unique_notes = set(all_notes.values())
    orphans = [n for n in unique_notes if len(inlinks[n]) == 0 and not n.startswith('00_Dashboard')]
    unique_canvases = set(all_canvases.values())
    unique_attachments = set(all_attachments.values())
    unused_media = [a for a in unique_attachments if len(inlinks[a]) == 0]

    return {
        "total_notes": len(unique_notes),
        "total_canvases": len(unique_canvases),
        "total_attachments": len(unique_attachments),
        "broken_links": broken_links,
        "broken_embeds": broken_embeds,
        "orphans": orphans,
        "unused_media": unused_media,
        "inlinks": inlinks,
        "outlinks": outlinks
    }

def main():
    parser = argparse.ArgumentParser(description="Obsidian Vault Link & Attachment Auditor")
    parser.add_argument("vault", nargs="?", default=".", help="Path to Obsidian vault root")
    parser.add_argument("--include-archive", action="store_true", help="Include _Archive directory in audit")
    args = parser.parse_args()

    vault_path = os.path.abspath(args.vault)
    if not os.path.isdir(vault_path):
        print(f"❌ Error: Vault directory does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Auditing Links & Attachments in: {vault_path}\n")
    res = audit_vault(vault_path, ignore_archive=not args.include_archive)

    print(f"📊 Vault Stats:")
    print(f"   Total Markdown Notes: {res['total_notes']}")
    print(f"   Total Canvases:       {res['total_canvases']}")
    print(f"   Total Attachments:    {res['total_attachments']}")
    print(f"   Broken Note Links:    {sum(len(v) for v in res['broken_links'].values())}")
    print(f"   Broken Image Embeds:  {sum(len(v) for v in res['broken_embeds'].values())}")
    print(f"   Orphan Notes:         {len(res['orphans'])}")
    print(f"   Unused Attachments:   {len(res['unused_media'])}\n")

    has_errors = False
    if res['broken_links']:
        has_errors = True
        print(f"❌ BROKEN NOTE LINKS ({len(res['broken_links'])} files):")
        for f, targets in res['broken_links'].items():
            print(f"   📄 {f}:")
            for t in targets:
                print(f"      • [[{t}]]")
        print()

    if res['broken_embeds']:
        has_errors = True
        print(f"❌ BROKEN IMAGE / FILE EMBEDS ({len(res['broken_embeds'])} files):")
        for f, targets in res['broken_embeds'].items():
            print(f"   📄 {f}:")
            for t in targets:
                print(f"      • ![[{t}]]")
        print()

    if res['orphans']:
        print(f"⚠️ ORPHAN NOTES ({len(res['orphans'])} files with no backlinks):")
        for o in sorted(res['orphans']):
            print(f"   • {o}")
        print()

    if res['unused_media']:
        print(f"ℹ️ UNUSED ATTACHMENTS ({len(res['unused_media'])} files):")
        for u in sorted(res['unused_media']):
            print(f"   • {u}")
        print()

    if not has_errors and not res['unused_media'] and not res['orphans']:
        print("🎉 Perfect Vault Graph! 0 broken links, 0 broken embeds, 0 orphans, 0 unused media.")

    if has_errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
