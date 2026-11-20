#!/usr/bin/env python3
"""
Obsidian Vault Linter & Syntax Validator
Scans markdown files for YAML frontmatter validity, broken pipes in table embeds,
unclosed brackets, malformed callouts, codeblock-trapped callouts, and formatting anomalies.
Supports --fix to automatically repair common syntax defects (e.g. escaped pipes, unwrapping callouts).
"""
import sys
import os
import re
import argparse
import yaml

ESCAPED_PIPE_RE = re.compile(r'(!?\[\[[^\]\n]*?)\\(\|)([^\]\n]*?\]\])')
UNCLOSED_WIKILINK_RE = re.compile(r'\[\[(?:(?!\]\])[^\n])*$')
MALFORMED_CALLOUT_RE = re.compile(r'^>\s*\[!([a-zA-Z0-9_\-]+)\]([^\+\-\s\n].*)$')
NON_COLLAPSIBLE_QUESTION_RE = re.compile(r'^>\s*\[!question\](\s+.*)$')
CODEBLOCK_CALLOUT_RE = re.compile(r'```(?:markdown)?\s*\n(>\s*\[!.*?\n(?:>.*?\n)*)```', re.MULTILINE)

def lint_file(file_path, auto_fix=False):
    issues = []
    fixed = False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"ERROR reading file: {e}"], False

    # Check 1: Frontmatter check
    if content.startswith('---\n') or content.startswith('---\r\n'):
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            fm_text = parts[1]
            try:
                yaml.safe_load(fm_text)
            except yaml.YAMLError as ye:
                issues.append(f"Line 1: Invalid YAML frontmatter: {ye}")
        else:
            issues.append("Line 1: Frontmatter opened with '---' but not properly closed with '---'.")
    else:
        # Warning: No frontmatter
        issues.append("Line 1: Note is missing YAML frontmatter (`---`).")

    new_content = content

    # Check 2: Escaped pipes in embeds/wikilinks (e.g. ![[image\|250]])
    if ESCAPED_PIPE_RE.search(new_content):
        matches = ESCAPED_PIPE_RE.findall(new_content)
        issues.append(f"Found {len(matches)} instance(s) of escaped pipe `\\|` inside wikilink/embed.")
        if auto_fix:
            new_content = ESCAPED_PIPE_RE.sub(r'\1|\3', new_content)
            fixed = True

    # Check 3: Callout trapped inside markdown code block
    if CODEBLOCK_CALLOUT_RE.search(new_content):
        matches = CODEBLOCK_CALLOUT_RE.findall(new_content)
        issues.append(f"Found {len(matches)} callout(s) wrapped inside code blocks (blocks active recall rendering).")
        if auto_fix:
            new_content = CODEBLOCK_CALLOUT_RE.sub(r'\1', new_content)
            fixed = True

    # Check 4: Line-by-line checks
    lines = new_content.splitlines(keepends=True)
    repaired_lines = []
    
    for idx, line in enumerate(lines, 1):
        modified_line = line
        
        # Check malformed callout (missing space or modifier)
        m_callout = MALFORMED_CALLOUT_RE.match(modified_line)
        if m_callout:
            ctype, rest = m_callout.groups()
            issues.append(f"Line {idx}: Callout missing space or folding indicator after `[!{ctype}]`")
            if auto_fix:
                modified_line = f"> [!{ctype}] {rest.strip()}\n"
                fixed = True

        # Check question callout missing collapsible modifier `-`
        m_q = NON_COLLAPSIBLE_QUESTION_RE.match(modified_line)
        if m_q:
            rest = m_q.group(1)
            issues.append(f"Line {idx}: Question callout is not collapsible (`> [!question]` should be `> [!question]-`)")
            if auto_fix:
                modified_line = f"> [!question]-{rest}"
                fixed = True

        # Unclosed wikilink on single line
        if '[[' in modified_line and ']]' not in modified_line:
            if not modified_line.strip().startswith('```') and not modified_line.strip().startswith('`'):
                if UNCLOSED_WIKILINK_RE.search(modified_line):
                    issues.append(f"Line {idx}: Potentially unclosed wikilink: {modified_line.strip()[:60]}")

        repaired_lines.append(modified_line)

    if auto_fix and fixed:
        new_content = "".join(repaired_lines)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

    return issues, fixed

def scan_vault(vault_dir, auto_fix=False, ignore_archive=True):
    total_files = 0
    clean_files = 0
    issues_found = 0
    fixed_files = 0
    report = []

    for root, dirs, files in os.walk(vault_dir):
        # Skip hidden and archive directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (ignore_archive and d.startswith('_Archive'))]
        for file in sorted(files):
            if file.endswith('.md'):
                total_files += 1
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, vault_dir)
                file_issues, was_fixed = lint_file(full_path, auto_fix=auto_fix)
                
                if was_fixed:
                    fixed_files += 1
                
                if file_issues:
                    issues_found += len(file_issues)
                    report.append((rel_path, file_issues, was_fixed))
                else:
                    clean_files += 1

    return total_files, clean_files, issues_found, fixed_files, report

def main():
    parser = argparse.ArgumentParser(description="Obsidian Vault Linter & Syntax Validator")
    parser.add_argument("vault", nargs="?", default=".", help="Path to Obsidian vault root")
    parser.add_argument("--fix", action="store_true", help="Automatically repair repairable syntax issues")
    parser.add_argument("--include-archive", action="store_true", help="Include _Archive directory in scan")
    args = parser.parse_args()

    vault_path = os.path.abspath(args.vault)
    if not os.path.isdir(vault_path):
        print(f"❌ Error: Vault directory does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Linting Obsidian Vault at: {vault_path}")
    print(f"⚡ Auto-fix mode: {'ENABLED' if args.fix else 'DISABLED'}\n")

    total, clean, issues, fixed, report = scan_vault(vault_path, auto_fix=args.fix, ignore_archive=not args.include_archive)

    for rel_path, file_issues, was_fixed in report:
        fix_badge = " [🛠️ FIXED]" if was_fixed else ""
        print(f"📄 {rel_path}{fix_badge}:")
        for issue in file_issues:
            print(f"   • {issue}")
        print()

    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   Total Markdown Files: {total}")
    print(f"   Clean Files:          {clean}")
    print(f"   Total Issues Noted:   {issues}")
    if args.fix:
        print(f"   Files Auto-Repaired:  {fixed}")
    print("=" * 60)

    if issues > 0 and not args.fix:
        sys.exit(1)

if __name__ == "__main__":
    main()
