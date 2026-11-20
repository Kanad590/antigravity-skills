#!/usr/bin/env python3
"""Universal Royal Pearl / Modern Dark Markdown-to-PDF renderer via Headless Chrome."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import markdown

MD_EXTENSIONS = ["extra", "tables", "fenced_code", "sane_lists"]

CALLOUT_THEMES = {
    "royal_pearl": {
        "abstract": {"title": "Executive Summary", "color": "#0F3D3E", "bg": "#FFFFFF", "border": "#C59B27", "icon": "🧠"},
        "summary": {"title": "Executive Summary", "color": "#0F3D3E", "bg": "#FFFFFF", "border": "#C59B27", "icon": "🧠"},
        "info": {"title": "Info", "color": "#0F3D3E", "bg": "#EFF6F6", "border": "#0F3D3E", "icon": "ℹ️"},
        "note": {"title": "Note", "color": "#0F3D3E", "bg": "#EFF6F6", "border": "#0F3D3E", "icon": "📝"},
        "tip": {"title": "Action Shortcut", "color": "#2E6F5E", "bg": "#E9F3F0", "border": "#2E6F5E", "icon": "💡"},
        "hint": {"title": "Action Shortcut", "color": "#2E6F5E", "bg": "#E9F3F0", "border": "#2E6F5E", "icon": "💡"},
        "success": {"title": "Verified", "color": "#2E6F5E", "bg": "#E9F3F0", "border": "#2E6F5E", "icon": "✅"},
        "warning": {"title": "Caution", "color": "#B84A39", "bg": "#FBECE9", "border": "#B84A39", "icon": "⚠️"},
        "caution": {"title": "Caution", "color": "#B84A39", "bg": "#FBECE9", "border": "#B84A39", "icon": "⚠️"},
        "danger": {"title": "Critical Trap", "color": "#B84A39", "bg": "#FBECE9", "border": "#B84A39", "icon": "🚨"},
        "important": {"title": "Important", "color": "#B84A39", "bg": "#FBECE9", "border": "#B84A39", "icon": "❗"},
        "question": {"title": "Active Recall", "color": "#0F3D3E", "bg": "#F4F1EA", "border": "#C59B27", "icon": "❓"},
    },
    "dark": {
        "abstract": {"title": "Executive Summary", "color": "#38BDF8", "bg": "#1E293B", "border": "#D4AF37", "icon": "🧠"},
        "summary": {"title": "Executive Summary", "color": "#38BDF8", "bg": "#1E293B", "border": "#D4AF37", "icon": "🧠"},
        "info": {"title": "Info", "color": "#38BDF8", "bg": "#1E293B", "border": "#38BDF8", "icon": "ℹ️"},
        "note": {"title": "Note", "color": "#38BDF8", "bg": "#1E293B", "border": "#38BDF8", "icon": "📝"},
        "tip": {"title": "Action Shortcut", "color": "#34D399", "bg": "#142E2A", "border": "#34D399", "icon": "💡"},
        "warning": {"title": "Caution", "color": "#FBBF24", "bg": "#2D2418", "border": "#FBBF24", "icon": "⚠️"},
        "danger": {"title": "Critical Trap", "color": "#F87171", "bg": "#321D22", "border": "#F87171", "icon": "🚨"},
        "question": {"title": "Active Recall", "color": "#D4AF37", "bg": "#1E293B", "border": "#D4AF37", "icon": "❓"},
    },
}


def detect_vault_root(input_path: Path, explicit_root: str | None) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    cur = input_path.resolve().parent
    for parent in [cur, *cur.parents]:
        if (parent / ".obsidian").is_dir() or (parent / ".git").is_dir():
            return parent
    return cur


def resolve_image_path(rel_or_abs: str, input_dir: Path, vault_root: Path) -> str:
    cleaned = rel_or_abs.strip()
    if re.match(r"^https?://|^file://|^data:", cleaned, re.IGNORECASE):
        return cleaned
    p = Path(cleaned)
    if p.is_absolute() and p.exists():
        return f"file://{p}"
    for base in (input_dir, vault_root, vault_root / "Assets 📦"):
        candidate = (base / cleaned).resolve()
        if candidate.exists():
            return f"file://{candidate}"
    # Fallback search by basename inside vault_root if wikilink omits folder
    if "/" not in cleaned:
        matches = list(vault_root.rglob(cleaned))
        if matches:
            return f"file://{matches[0].resolve()}"
    return f"file://{(vault_root / cleaned).resolve()}"


def convert_image_embeds(text: str, input_dir: Path, vault_root: Path) -> str:
    def obsidian_img_repl(m: re.Match[str]) -> str:
        rel = m.group(1).strip()
        src = resolve_image_path(rel, input_dir, vault_root)
        return f'<img src="{html.escape(src)}" class="vault-img" alt="{html.escape(os.path.basename(rel))}"/>'

    def md_img_repl(m: re.Match[str]) -> str:
        alt = m.group(1).strip()
        rel = m.group(2).strip()
        src = resolve_image_path(rel, input_dir, vault_root)
        return f'<img src="{html.escape(src)}" class="vault-img" alt="{html.escape(alt)}"/>'

    # MUST run BEFORE strip_wikilinks so ![[img|220]] does not become !<strong>220</strong>
    text = re.sub(r"!\[\[([^|\]]+)(?:\|[^\]]+)?\]\]", obsidian_img_repl, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", md_img_repl, text)
    return text


def strip_wikilinks(text: str, input_dir: Path, vault_root: Path) -> str:
    text = convert_image_embeds(text, input_dir, vault_root)
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"<strong>\2</strong>", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"<strong>\1</strong>", text)
    return text


def render_dataviewjs_quiz(code: str) -> str:
    items = re.findall(
        r'\{\s*q:\s*"(.*?)",\s*a:\s*"(.*?)",\s*why:\s*"(.*?)"\s*\}',
        code,
        flags=re.DOTALL,
    )
    if not items:
        return '<div class="callout" style="border-left-color:#C59B27;"><div class="callout-body"><em>[Interactive DataviewJS view omitted in print PDF]</em></div></div>'
    cards = ['<div class="quiz-grid">']
    for q, a, why in items:
        cards.append(
            f"""<div class="quiz-card">
  <div class="quiz-q">{html.escape(q)}</div>
  <div class="quiz-a"><span class="pill pill-sage">✅ Answer</span> {html.escape(a)}</div>
  <div class="quiz-why">💡 {html.escape(why)}</div>
</div>"""
        )
    cards.append("</div>")
    return "\n".join(cards)


def convert_flashcards(md_text: str) -> str:
    pattern = re.compile(
        r"#flashcards/[^\n]+\n\*\*Question:\*\*\s*(.*?)\n\?\n\*\*Answer:\*\*\s*(.*?)\n\*\*Logic[^\n]*?:\*\*\s*(.*?)(?=\n\n|\Z)",
        flags=re.DOTALL,
    )

    def repl(m: re.Match[str]) -> str:
        q_html = markdown.markdown(m.group(1).strip(), extensions=MD_EXTENSIONS)
        a_html = markdown.markdown(m.group(2).strip(), extensions=MD_EXTENSIONS)
        l_html = markdown.markdown(m.group(3).strip(), extensions=MD_EXTENSIONS)
        return (
            f'\n<div class="flashcard">\n'
            f'  <div class="fc-q"><span class="pill pill-gold">FLASHCARD</span> {q_html}</div>\n'
            f'  <div class="fc-a"><strong>✅ Answer:</strong> {a_html}</div>\n'
            f'  <div class="fc-l"><strong>💡 Logic:</strong> {l_html}</div>\n'
            f"</div>\n"
        )

    return pattern.sub(repl, md_text)


def parse_markdown(md_text: str, input_path: Path, vault_root: Path, theme: str):
    frontmatter: dict[str, str] = {}
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            md_text = parts[2].lstrip("\n")
            for line in fm_text.splitlines():
                if ":" in line and not line.startswith(" "):
                    k, v = line.split(":", 1)
                    frontmatter[k.strip()] = v.strip().strip("\"'")

    h1_match = re.match(r"^#\s+(.+)\n+", md_text)
    doc_heading = frontmatter.get("title", input_path.stem)
    if h1_match:
        doc_heading = h1_match.group(1).strip()
        md_text = md_text[h1_match.end():]
    doc_heading = re.sub(r"`([^`]+)`", r"<code>\1</code>", doc_heading)

    # Guard nested *... **...*** against crossing table pipes |
    md_text = re.sub(r"\*([^*\n|]+?)\*\*([^*\n|]+?)\*\*\*", r"<em>\1<strong>\2</strong></em>", md_text)
    md_text = md_text.replace("(`DataviewJS` — মুখস্থ না করে যাচাই করো)", "(প্রশ্ন ও উত্তর)")

    mermaid_blocks: list[str] = []

    def mermaid_repl(m: re.Match[str]) -> str:
        idx = len(mermaid_blocks)
        code = m.group(1).strip()
        # Wide top-down trees shrink too small on A4 portrait; flip to LR for legibility
        if code.startswith("flowchart TD") and code.count("-->") >= 6:
            code = re.sub(r"^flowchart\s+TD", "flowchart LR", code)
        mermaid_blocks.append(code)
        return f"\n\n<!--MERMAID_BLOCK_{idx}-->\n\n"

    md_text = re.sub(r"```mermaid\s*\n(.*?)\n```", mermaid_repl, md_text, flags=re.DOTALL)

    dv_blocks: list[str] = []

    def dv_repl(m: re.Match[str]) -> str:
        idx = len(dv_blocks)
        dv_blocks.append(render_dataviewjs_quiz(m.group(1)))
        return f"\n\n<!--DV_BLOCK_{idx}-->\n\n"

    md_text = re.sub(r"```dataviewjs\s*\n(.*?)\n```", dv_repl, md_text, flags=re.DOTALL)
    md_text = re.sub(r"```dataview\s*\n.*?\n```", "", md_text, flags=re.DOTALL)

    md_text = convert_flashcards(md_text)

    # LaTeX Math protection (extract before callout & markdown processing)
    math_blocks: list[str] = []

    def math_block_repl(m: re.Match[str]) -> str:
        idx = len(math_blocks)
        raw_code = m.group(1).strip()
        lines = [re.sub(r"^>\s?", "", l) for l in raw_code.splitlines()]
        code = "\n".join(lines).strip()
        math_blocks.append(code)
        return f"<!--MATH_BLOCK_{idx}-->"

    # Match block math $$...$$ and \[...\]
    md_text = re.sub(r"\$\$\s*\n?(.*?)\n?\$\$", math_block_repl, md_text, flags=re.DOTALL)
    md_text = re.sub(r"\\\[\s*\n?(.*?)\n?\\\]", math_block_repl, md_text, flags=re.DOTALL)

    math_inlines: list[str] = []

    def math_inline_repl(m: re.Match[str]) -> str:
        idx = len(math_inlines)
        math_inlines.append(m.group(1).strip())
        return f"<!--MATH_INLINE_{idx}-->"

    # Match inline math $...$ (avoid escaped \$) and \(...\)
    md_text = re.sub(r"(?<!\\)\$(?!\s)([^\$\n]+?)(?<!\s)\$", math_inline_repl, md_text)
    md_text = re.sub(r"\\\(\s*(.*?)\s*\\\)", math_inline_repl, md_text)

    cfg_map = CALLOUT_THEMES.get(theme, CALLOUT_THEMES["royal_pearl"])
    input_dir = input_path.parent
    lines = md_text.splitlines()
    out_lines: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^>\s*\[!(\w+)\][-+]?\s*(.*)$", line)
        if m:
            ctype = m.group(1).lower()
            ctitle = strip_wikilinks(m.group(2).strip(), input_dir, vault_root)
            cfg = cfg_map.get(ctype, cfg_map["note"])
            has_emoji = bool(re.search(r"[\U00010000-\U0010ffff\u2600-\u27bf]", ctitle))
            icon_html = f'<span class="callout-icon">{cfg["icon"]}</span>' if not has_emoji else ""
            display_title = (
                markdown.markdown(ctitle, extensions=MD_EXTENSIONS).replace("<p>", "").replace("</p>", "")
                if ctitle
                else cfg["title"]
            )

            body_lines: list[str] = []
            i += 1
            while i < len(lines):
                cur = lines[i]
                if cur.startswith(">"):
                    if re.match(r"^>\s*\[!\w+\]", cur):
                        break
                    body_lines.append(re.sub(r"^>\s?", "", cur))
                    i += 1
                elif (
                    cur.strip() == ""
                    and i + 1 < len(lines)
                    and lines[i + 1].startswith(">")
                    and not re.match(r"^>\s*\[!\w+\]", lines[i + 1])
                ):
                    body_lines.append("")
                    i += 1
                else:
                    break

            body_raw = "\n".join(body_lines)
            body_raw = re.sub(r"([^\n])\n(\* |- |\d+\. )", r"\1\n\n\2", body_raw)
            body_md = strip_wikilinks(body_raw, input_dir, vault_root)
            body_html = markdown.markdown(body_md, extensions=MD_EXTENSIONS)
            callout_html = (
                f'<div class="callout" style="border-left-color: {cfg["border"]}; background-color: {cfg["bg"]};">\n'
                f'  <div class="callout-header" style="color: {cfg["color"]};">{icon_html}<span class="callout-title">{display_title}</span></div>\n'
                f'  <div class="callout-body">{body_html}</div>\n'
                f"</div>"
            )
            out_lines.append(callout_html)
        else:
            out_lines.append(line)
            i += 1

    md_text = "\n".join(out_lines)
    md_text = re.sub(r"==(.*?)==", r"<mark>\1</mark>", md_text)
    md_text = strip_wikilinks(md_text, input_dir, vault_root)

    # Extract h2 section headings for dynamic At-a-Glance fallback
    h2_headings = [re.sub(r"`([^`]+)`", r"\1", h.strip()) for h in re.findall(r"^##\s+(.+)$", md_text, flags=re.MULTILINE)]

    html_body = markdown.markdown(md_text, extensions=MD_EXTENSIONS)

    for idx, dv_html in enumerate(dv_blocks):
        html_body = html_body.replace(f"<p><!--DV_BLOCK_{idx}--></p>", dv_html)
        html_body = html_body.replace(f"<!--DV_BLOCK_{idx}-->", dv_html)

    for idx, code in enumerate(mermaid_blocks):
        m_html = f'<div class="mermaid-box"><div class="mermaid">\n{code}\n</div></div>'
        html_body = html_body.replace(f"<p><!--MERMAID_BLOCK_{idx}--></p>", m_html)
        html_body = html_body.replace(f"<!--MERMAID_BLOCK_{idx}-->", m_html)

    for idx, code in enumerate(math_blocks):
        m_html = f'<div class="katex-block">$$\n{code}\n$$</div>'
        html_body = html_body.replace(f"<p><!--MATH_BLOCK_{idx}--></p>", m_html)
        html_body = html_body.replace(f"<!--MATH_BLOCK_{idx}-->", m_html)

    for idx, code in enumerate(math_inlines):
        m_html = f'<span class="katex-inline">${code}$</span>'
        html_body = html_body.replace(f"<!--MATH_INLINE_{idx}-->", m_html)

    return doc_heading, frontmatter, h2_headings, html_body


def load_json_arg(raw: str | None) -> Any:
    if not raw:
        return None
    p = Path(raw)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    if raw.startswith("/") or raw.endswith(".json"):
        if not p.exists():
            raise FileNotFoundError(f"JSON file not found: {raw}")
    return json.loads(raw)


def build_kpi_html(frontmatter: dict[str, str], h2_headings: list[str], kpi_data: list[dict[str, str]] | None) -> str:
    if not kpi_data:
        subj = frontmatter.get("subject", "Executive Brief")
        topic = frontmatter.get("topic", frontmatter.get("status", "Verified Guide"))
        date_str = frontmatter.get("date", "Current Edition")
        sec_preview = " • ".join(h2_headings[:2]) if h2_headings else "Structured Visual Reference"
        if len(sec_preview) > 85:
            sec_preview = sec_preview[:82].rsplit(" ", 1)[0] + "…"
        kpi_data = [
            {"label": "📌 Focus Domain", "val": subj, "desc": topic},
            {"label": "🗂️ Coverage", "val": f"{max(len(h2_headings), 1)} Sections", "desc": sec_preview},
            {"label": "📅 Edition", "val": date_str, "desc": "Scannable Executive Layout • Print & Mobile Ready"},
        ]
    cards = []
    for item in kpi_data[:3]:
        cards.append(
            f"""<div class="kpi-card">
      <div class="kpi-label">{html.escape(str(item.get("label", "")))}</div>
      <div class="kpi-val">{html.escape(str(item.get("val", "")))}</div>
      <div class="kpi-desc">{html.escape(str(item.get("desc", "")))}</div>
    </div>"""
        )
    return f'<div class="kpi-grid">\n{"".join(cards)}\n</div>'


def build_cheat_sheet_html(cheat_data: dict[str, Any] | None, include_sheet: bool) -> str:
    if not include_sheet or not cheat_data:
        return ""
    title = html.escape(str(cheat_data.get("title", "⚡ Action Cheat Sheet (Do's & Don'ts)")))
    dos = "".join(f"<li>{item}</li>" for item in cheat_data.get("dos", []))
    donts = "".join(f"<li>{item}</li>" for item in cheat_data.get("donts", []))
    next_step = cheat_data.get("next_step", "")
    next_html = f'<div class="next-step-bar">🎯 <strong>Next Step:</strong> {next_step}</div>' if next_step else ""
    return f"""
<div class="action-sheet">
  <div class="action-sheet-header">
    <span class="pill pill-gold">ONE-PAGE ACTION CHEAT SHEET</span>
    <h2>{title}</h2>
  </div>
  <div class="dos-donts-grid">
    <div class="do-card">
      <div class="card-title">✅ DO's (Best Practices)</div>
      <ul>{dos}</ul>
    </div>
    <div class="dont-card">
      <div class="card-title">⚠️ DON'Ts (Avoid Traps)</div>
      <ul>{donts}</ul>
    </div>
  </div>
  {next_html}
</div>
"""


def build_css(theme: str, footer_left: str) -> str:
    if theme == "dark":
        page_bg, card_bg, text_col, muted_col = "#111827", "#1E293B", "#F1F5F9", "#94A3B8"
        head_bg, head_text, accent, border_col = "#0F172A", "#F8FAFC", "#D4AF37", "#334155"
        th_bg, th_text, even_row, code_bg, code_col = "#0F172A", "#38BDF8", "#162032", "#0F172A", "#38BDF8"
        do_bg, do_border, do_title = "#142E2A", "#2E6F5E", "#34D399"
        dont_bg, dont_border, dont_title = "#321D22", "#B84A39", "#F87171"
        mermaid_vars = "primaryColor:'#1E293B',primaryTextColor:'#F1F5F9',primaryBorderColor:'#38BDF8',lineColor:'#D4AF37'"
    else:
        # Royal Pearl & Deep Teal + Warm Gold (Default)
        page_bg, card_bg, text_col, muted_col = "#FAF8F4", "#FFFFFF", "#222831", "#475569"
        head_bg, head_text, accent, border_col = "#0F3D3E", "#FAF8F4", "#C59B27", "#E2D9C5"
        th_bg, th_text, even_row, code_bg, code_col = "#0F3D3E", "#FAF8F4", "#F7F4EC", "#EFECE4", "#0F3D3E"
        do_bg, do_border, do_title = "#E9F3F0", "#B7DEC9", "#2E6F5E"
        dont_bg, dont_border, dont_title = "#FBECE9", "#E9B9B0", "#B84A39"
        mermaid_vars = "primaryColor:'#E9F3F0',primaryTextColor:'#0F3D3E',primaryBorderColor:'#0F3D3E',lineColor:'#C59B27'"

    safe_footer = footer_left.replace('"', "'")
    return f"""
    @page {{
      size: A4 portrait;
      margin: 12mm 13mm 13mm 13mm;
      background-color: {page_bg};
      @bottom-left {{
        content: "{safe_footer}";
        font-family: 'Plus Jakarta Sans', 'Noto Sans Bengali', 'Noto Sans Devanagari', 'Lohit Bengali', sans-serif;
        font-size: 7.5pt;
        color: {muted_col};
      }}
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 7.5pt;
        font-weight: 600;
        color: {accent};
      }}
    }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
    html, body {{
      background-color: {page_bg};
      color: {text_col};
      font-family: 'Plus Jakarta Sans', 'Noto Sans Bengali', 'Noto Sans Devanagari', 'Lohit Bengali', 'Noto Color Emoji', sans-serif;
      font-size: 9.2pt;
      line-height: 1.54;
      margin: 0;
      padding: 0;
    }}
    .hero-banner {{
      background: linear-gradient(135deg, {head_bg} 0%, #13293D 100%);
      color: {head_text};
      border-radius: 10px;
      padding: 14px 18px 13px 18px;
      margin-bottom: 11px;
      border-bottom: 3.5px solid {accent};
    }}
    .badge-bar {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 7px; }}
    .badge {{
      display: inline-block; font-size: 7.2pt; font-weight: 700; letter-spacing: 0.5px;
      text-transform: uppercase; padding: 2px 8px; border-radius: 999px;
      background: rgba(197, 155, 39, 0.22); color: #F6DF96; border: 1px solid rgba(197, 155, 39, 0.55);
    }}
    .hero-banner h1 {{
      font-family: 'Playfair Display', 'Noto Sans Bengali', 'Noto Sans Devanagari', serif;
      font-size: 16.5pt; font-weight: 800; color: #FFFFFF; margin: 0 0 4px 0; line-height: 1.24;
    }}
    .hero-banner h1 code {{
      background: rgba(197, 155, 39, 0.25); color: #FDE68A; border: 1px solid rgba(197, 155, 39, 0.5);
      font-size: 12.5pt; padding: 1px 6px; border-radius: 5px;
    }}
    .hero-sub {{ font-size: 8.3pt; color: #CBD5E1; margin: 0; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px; }}
    .kpi-card {{
      background: {card_bg}; border: 1px solid {border_col}; border-top: 3px solid {accent};
      border-radius: 8px; padding: 8px 10px;
    }}
    .kpi-label {{ font-size: 7.2pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; color: {accent}; margin-bottom: 2px; }}
    .kpi-val {{ font-size: 10.6pt; font-weight: 800; color: {text_col}; margin-bottom: 2px; }}
    .kpi-desc {{ font-size: 7.8pt; color: {muted_col}; line-height: 1.35; }}
    h2 {{
      font-size: 11.8pt; font-weight: 800; color: {accent if theme == "dark" else "#0F3D3E"};
      border-bottom: 1.5px solid {border_col}; padding-bottom: 3px; margin: 15px 0 8px 0;
      break-after: avoid; page-break-after: avoid;
    }}
    h3 {{ font-size: 10.2pt; font-weight: 700; color: {text_col}; margin: 11px 0 6px 0; break-after: avoid; page-break-after: avoid; }}
    p {{ margin: 0 0 7px 0; }}
    ul, ol {{ margin: 0 0 7px 0; padding-left: 18px; }}
    li {{ margin-bottom: 3px; }}
    table {{
      width: 100%; border-collapse: separate; border-spacing: 0; font-size: 8.3pt; margin: 8px 0 12px 0;
      border: 1px solid {border_col}; border-radius: 8px; overflow: hidden; background: {card_bg};
    }}
    thead {{ display: table-header-group; }}
    tr {{ break-inside: avoid; page-break-inside: avoid; }}
    th {{
      background-color: {th_bg}; color: {th_text}; font-weight: 700; text-align: left;
      padding: 6px 8px; border-bottom: 2px solid {accent}; border-right: 1px solid rgba(255,255,255,0.12);
    }}
    th:last-child {{ border-right: none; }}
    td {{ padding: 5.5px 8px; border-bottom: 1px solid {border_col}; border-right: 1px solid {border_col}; vertical-align: top; color: {text_col}; }}
    td:last-child {{ border-right: none; }}
    tbody tr:last-child td {{ border-bottom: none; }}
    tbody tr:nth-child(even) td {{ background-color: {even_row}; }}
    .vault-img {{ display: block; width: 100%; height: auto; max-height: 900px; object-fit: contain; border-radius: 6px; border: 1px solid {border_col}; margin: 8px auto; }}
    .callout {{
      border: 1px solid {border_col}; border-left: 4px solid {accent}; border-radius: 8px;
      padding: 8px 11px; margin: 9px 0 11px 0; break-inside: avoid; page-break-inside: avoid;
    }}
    .callout-header {{ display: flex; align-items: center; gap: 6px; font-weight: 700; font-size: 9.3pt; margin-bottom: 4px; }}
    .callout-body {{ font-size: 8.7pt; line-height: 1.48; color: {text_col}; }}
    .callout-body p:last-child, .callout-body ul:last-child {{ margin-bottom: 0; }}
    mark {{ background-color: #FEF3C7; color: #78350F; padding: 0 3px; border-radius: 3px; font-weight: 600; }}
    code {{
      font-family: 'Fira Code', 'DejaVu Sans Mono', monospace; background-color: {code_bg};
      padding: 1px 4px; border-radius: 4px; font-size: 8.1pt; color: {code_col}; border: 1px solid {border_col};
    }}
    .mermaid-box {{
      margin: 9px 0 11px 0; padding: 8px; border: 1px solid {border_col}; border-radius: 8px;
      text-align: center; background: {card_bg}; break-inside: avoid; page-break-inside: avoid;
    }}
    .mermaid svg {{ max-width: 100% !important; max-height: 410px !important; height: auto !important; }}
    .katex-block {{
      margin: 4px 0 6px 0; padding: 4px 8px; border: 1px solid {border_col}; border-radius: 6px;
      text-align: center; background: {card_bg}; break-inside: avoid; page-break-inside: avoid;
    }}
    .katex-display {{ margin: 0 !important; }}
    .katex {{ font-size: 1.04em; }}
    .pill {{ display: inline-block; font-size: 7pt; font-weight: 700; letter-spacing: 0.3px; padding: 1px 6px; border-radius: 999px; margin-right: 4px; vertical-align: middle; }}
    .pill-sage {{ background: {do_bg}; color: {do_title}; border: 1px solid {do_border}; }}
    .pill-gold {{ background: #FEF3C7; color: #92400E; border: 1px solid #E5C158; }}
    .quiz-grid {{ display: flex; flex-direction: column; gap: 6px; margin: 7px 0 10px 0; }}
    .quiz-card {{
      border: 1px solid {border_col}; border-left: 4px solid #2E6F5E; border-radius: 8px;
      padding: 7px 10px; background: {card_bg}; break-inside: avoid; page-break-inside: avoid; font-size: 8.6pt;
    }}
    .quiz-q {{ font-weight: 700; color: {text_col}; margin-bottom: 3px; }}
    .quiz-a {{ color: {do_title}; margin-bottom: 2px; }}
    .quiz-why {{ color: {muted_col}; font-size: 8.2pt; }}
    .flashcard {{
      border: 1px solid {border_col}; border-left: 4px solid {accent}; border-radius: 8px;
      padding: 6px 10px; margin: 6px 0; background: {card_bg}; break-inside: avoid; page-break-inside: avoid; font-size: 8.5pt;
    }}
    .flashcard p {{ display: inline; margin: 0; }}
    .fc-q {{ margin-bottom: 3px; color: {text_col}; font-weight: 600; }}
    .fc-a {{ margin-bottom: 2px; color: {do_title}; }}
    .fc-l {{ color: {muted_col}; font-size: 8.1pt; }}
    .action-sheet {{
      margin-top: 12px; background: {card_bg}; border: 1.5px solid {accent}; border-radius: 10px;
      padding: 11px 13px; break-inside: avoid; page-break-inside: avoid;
    }}
    .action-sheet-header h2 {{ margin: 4px 0 8px 0; border-bottom-color: {border_col}; }}
    .dos-donts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 9px; margin-bottom: 8px; }}
    .do-card {{ background: {do_bg}; border: 1px solid {do_border}; border-radius: 8px; padding: 8px 10px; font-size: 8.1pt; }}
    .do-card .card-title {{ font-weight: 800; color: {do_title}; margin-bottom: 4px; font-size: 8.8pt; }}
    .dont-card {{ background: {dont_bg}; border: 1px solid {dont_border}; border-radius: 8px; padding: 8px 10px; font-size: 8.1pt; }}
    .dont-card .card-title {{ font-weight: 800; color: {dont_title}; margin-bottom: 4px; font-size: 8.8pt; }}
    .do-card ul, .dont-card ul {{ margin: 0; padding-left: 15px; }}
    .do-card li, .dont-card li {{ margin-bottom: 3px; line-height: 1.4; }}
    .next-step-bar {{
      background: {head_bg}; color: {head_text}; border-radius: 6px; padding: 6px 10px;
      font-size: 8.3pt; border-left: 4px solid {accent};
    }}
    hr {{ border: none; border-top: 1px dashed {border_col}; margin: 11px 0; }}
    <!--MERMAID_THEME_VARS:{mermaid_vars}-->
    """


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown/Obsidian notes into Royal Pearl A4 PDFs via Headless Chrome.")
    parser.add_argument("--input", "-i", required=True, help="Path to source .md file")
    parser.add_argument("--output", "-o", required=True, help="Path to output .pdf file")
    parser.add_argument("--theme", choices=["royal_pearl", "dark"], default="royal_pearl", help="Color palette theme")
    parser.add_argument("--title", default=None, help="Override hero banner title")
    parser.add_argument("--subtitle", default=None, help="Hero subtitle")
    parser.add_argument("--badge", action="append", default=[], help="Hero badge (repeatable)")
    parser.add_argument("--footer", default=None, help="Bottom-left footer label")
    parser.add_argument("--vault-root", default=None, help="Base folder for resolving ![[...]] & relative images")
    parser.add_argument("--kpi-json", default=None, help="JSON string or file with 3 KPI dicts {label,val,desc}")
    parser.add_argument("--cheat-sheet-json", default=None, help="JSON string or file with {title,dos,donts,next_step}")
    parser.add_argument("--no-cheat-sheet", action="store_true", help="Omit the bottom action cheat sheet block")
    parser.add_argument("--qa-dir", default=None, help="Render 150-dpi PNGs into this folder via pdftoppm for visual QA")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    vault_root = detect_vault_root(input_path, args.vault_root)
    md_text = input_path.read_text(encoding="utf-8")

    doc_heading, fm, h2_headings, html_body = parse_markdown(md_text, input_path, vault_root, args.theme)
    title_html = args.title if args.title else doc_heading
    badges = args.badge or [
        f"📄 {fm.get('subject', 'EXECUTIVE DOCUMENT').upper()}",
        f"✨ {'MODERN DARK' if args.theme == 'dark' else 'ROYAL PEARL EDITION'}",
    ]
    badges_html = "\n      ".join(f'<span class="badge">{html.escape(b)}</span>' for b in badges)
    subtitle = args.subtitle or f"{fm.get('topic', input_path.stem)} • Scannable Executive Layout"
    footer_left = args.footer or f"{fm.get('subject', 'Gov-Exam-Prep')} • Royal Pearl Edition"

    kpi_data = load_json_arg(args.kpi_json)
    kpi_html = build_kpi_html(fm, h2_headings, kpi_data)
    cheat_data = load_json_arg(args.cheat_sheet_json)
    cheat_html = build_cheat_sheet_html(cheat_data, not args.no_cheat_sheet)

    css_text = build_css(args.theme, footer_left)
    m_match = re.search(r"<!--MERMAID_THEME_VARS:(.*?)-->", css_text)
    mermaid_vars = m_match.group(1) if m_match else ""
    css_text = re.sub(r"<!--MERMAID_THEME_VARS:.*?-->", "", css_text)

    full_html = f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(re.sub(r'<[^>]+>', '', title_html))}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      securityLevel: 'loose',
      flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis', nodeSpacing: 18, rankSpacing: 32 }},
      themeVariables: {{ fontFamily: 'Plus Jakarta Sans, Noto Sans Bengali, Lohit Bengali, sans-serif', fontSize: '11.5px', {mermaid_vars} }}
    }});
    document.addEventListener("DOMContentLoaded", function() {{
      if (typeof renderMathInElement === "function") {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{left: "$$", right: "$$", display: true}},
            {{left: "$", right: "$", display: false}},
            {{left: "\\\\(", right: "\\\\)", display: false}},
            {{left: "\\\\[", right: "\\\\]", display: true}}
          ],
          throwOnError: false
        }});
      }}
    }});
  </script>
  <style>{css_text}</style>
</head>
<body>
  <div class="hero-banner">
    <div class="badge-bar">
      {badges_html}
    </div>
    <h1>{title_html}</h1>
    <p class="hero-sub">{html.escape(subtitle)}</p>
  </div>
  {kpi_html}
  {html_body}
  {cheat_html}
</body>
</html>"""

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(full_html)
        tmp_html = tmp.name

    try:
        cmd = [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={output_path}",
            tmp_html,
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not output_path.exists() or output_path.stat().st_size == 0:
            raise RuntimeError(f"Chrome PDF generation failed: {res.stderr}")
        print(f"PDF_CREATED: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")

        if args.qa_dir:
            qa_path = Path(args.qa_dir).expanduser().resolve()
            qa_path.mkdir(parents=True, exist_ok=True)
            for old in qa_path.glob("qa_page*.png"):
                old.unlink()
            subprocess.run(["pdftoppm", "-r", "150", "-png", str(output_path), str(qa_path / "qa_page")], check=True)
            pages = sorted(p.name for p in qa_path.glob("qa_page*.png"))
            print(f"QA_PAGES: {pages}")
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)


if __name__ == "__main__":
    main()
