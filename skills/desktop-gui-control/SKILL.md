---
name: desktop-gui-control
description: >-
  Use this skill whenever the user asks to automate, control, click, type, or interact with desktop GUI applications on Pop!_OS (COSMIC Wayland or Xwayland),
  including Tuta Mail, JHora (Jagannatha Hora in Wine), browsers, terminal windows, media players, or native system apps.
  Provides Wayland-native input simulation (wtype, kernel evdev UInput pointer/wheel), fast clean screenshotting (cosmic-screenshot),
  AT-SPI accessibility widget discovery, Set-of-Mark visual tagging, Focus Guard safety, and single-call batch macro execution.
---

# Desktop GUI Control & Automation Skill (Pop!_OS COSMIC Wayland — v2.1)

This skill provides high-speed, deterministic desktop GUI automation, Wayland-native mouse/keyboard control, AT-SPI widget discovery, Set-of-Mark visual tagging, and Focus Guard protection for Pop!_OS 24.04 LTS (COSMIC Desktop, Wayland session `wayland-1`).

---

## 🖥️ System Architecture & Protocols

Property | Configuration
 :--- | :---
**OS / Desktop** | Pop!_OS 24.04 LTS (COSMIC Desktop / `cosmic-comp`)
**Display & D-Bus** | `WAYLAND_DISPLAY=wayland-1`, `DISPLAY=:1`, anchored to `/run/user/$UID/bus`
**Screenshots** | `cosmic-screenshot --interactive=false --notify=false -s /tmp` (~77ms, auto-moved to target with zero `/tmp` leak)
**Pointer & Wheel** | Kernel `/dev/uinput` via `evdev.UInput` (`ag-virtual-pointer` absolute tablet + `ag-virtual-wheel` relative scroll) — works identically on Wayland & Xwayland
**Keyboard Emulation** | `/usr/bin/wtype` with automatic XKB key alias normalization (`enter`→`Return`, `esc`→`Escape`) & stdin-safe multiline typing
**Window Maximize** | Idempotent `wmctrl` (Xwayland) + `Super+m` / `Super+F11` (COSMIC Wayland) with bounds check so already-maximized windows never toggle off
**Focus & Popup Guard** | `is_window_focused` (X11 `WM_CLASS` + AT-SPI `ACTIVE`) aborts input before typing into the wrong window; `stop_on_popup` halts when unexpected modal dialogs appear
**Set-of-Mark (SoM)** | `som_inspect` draws `[1]`, `[2]`, ... badges and caches exact screen coordinates for zero-guess `click_mark(id)`
**Accessibility & OCR** | AT-SPI (`toolkit-accessibility=true`, ~50–250ms) + Tesseract 5 (`OMP_THREAD_LIMIT=2`, dark-mode auto-invert, `--psm 11`, ranked scoring)
**CLI & MCP Hub** | `ag-gui` (`~/.local/bin/ag-gui`) loaded **in-process** by `linux-desktop-apps-mcp` (34 tools, 0ms subprocess overhead)

---

## ⚡ High-Speed Safety & Execution Rules

1. **Focus + Maximize First:** Always focus and maximize the target application (`gui_focus_window(title, maximize=True)` or `gui_maximize_window(title)`) before automating forms so background apps (like Antigravity IDE) are covered and UI controls stay full-sized.
2. **Always Set `guard_window` & `stop_on_popup` in `gui_batch`:** Pass `guard_window="AppName"` so typing immediately aborts if focus shifts away, and `stop_on_popup=True` when filling forms so validation popups halt execution safely.
3. **Never Eyeball Coordinates — Use Set-of-Mark (`gui_som_inspect` → `gui_click_mark`):** For unfamiliar dialogs or custom UIs (e.g. JHora/Wine), call `gui_som_inspect("App")` once to get numbered badges `[1]`, `[2]` and exact centers, then click via `gui_click_mark(id)`.
4. **Use `gui_replace_text` for Input Fields:** Especially in Wine/Win32 apps where `Ctrl+A` fails, `gui_replace_text` uses mouse drag-select + `BackSpace` before typing so values never concatenate (`2026` + `1999`).
5. **Prefer `gui_click_element` (AT-SPI) over OCR:** For native GTK/Qt/Firefox/Telegram apps, AT-SPI clicks in ~50–250ms with zero OCR overhead, automatically falling back to Smart OCR when needed.

---

## 🛠️ FastMCP High-Level Tools (`linux-desktop-apps`)

Tool | Parameters | Description
 :--- | :--- | :---
`gui_batch` | `steps`, `guard_window=None`, `stop_on_popup=False` | Executes an entire sequence (`focus`, `maximize`, `click`, `click_element`, `click_text`, `click_mark`, `replace_text`, `drag`, `scroll`, `type`, `key`, `hotkey`, `wait`, `wait_text`, `wait_change`, `screenshot`, `copy_image`) with Focus Guard & Popup Guard.
`gui_focus_window` | `title`, `maximize=False` | Focuses window and optionally maximizes it.
`gui_maximize_window` | `window_title=None`, `fullscreen=False` | Idempotently maximizes or fullscreens target/active window.
`gui_som_inspect` | `window_title=None` | Draws numbered `[1]`, `[2]`, ... badges on `/tmp/ag_som.png` and caches exact coordinates.
`gui_click_mark` | `mark_id`, `button="left"`, `double=False` | Clicks a cached Set-of-Mark ID (`[1]`, `[2]`, ...).
`gui_replace_text` | `text`, `x=None`, `y=None`, `width=90` | Safely clears existing text (Win32/Wine drag-select + `BackSpace` or `Ctrl+A`) and types new value.
`gui_find_elements` | `query=None`, `window_title=None` | Discovers visible UI widgets via AT-SPI with exact centers (~50–250ms).
`gui_click_element` | `query`, `window_title=None`, `button="left"`, `double=False` | Clicks via AT-SPI first, auto-falling back to fast Smart OCR.
`gui_smart_click` | `target`, `window=None`, `button="left"`, `double=False` | Coordinate string (`"500, 300"`) with visual delta verify, or text via AT-SPI + Smart OCR.
`gui_inspect_window` | `window_title=None` | Returns AT-SPI widgets + line-grouped OCR UI labels with exact boxes.
`gui_visual_grid_inspect` | `window_title=None` | Overlays coordinate grid (`A1..Z10`) on target window (~23 KB) for icon-only or canvas apps.
`gui_scroll` | `amount`, `x=None`, `y=None` | Native Wayland + Xwayland mouse wheel scroll via kernel `UInput`.
`gui_drag_and_drop` | `start_x`, `start_y`, `end_x`, `end_y`, `duration=0.5` | Smooth Wayland + Xwayland drag-and-drop via kernel `UInput`.
`gui_wait_for` | `text=None`, `window_title=None`, `timeout=10` | Pixel-diff-gated wait for text, window, or visual UI change.
`gui_copy_image_to_clipboard` | `image_path` | Stages PNG image to Wayland clipboard (`wl-copy`, zero pipe hang).
`gui_get_display_info` | *none* | Clean `cosmic-randr` display heads, modes, and scaling (ANSI-stripped).

---

## ⚡ Core CLI Commands (`ag-gui`)

Command | Description
 :--- | :---
`ag-gui batch '<json>' [--guard App] [--stop-on-popup]` | Run multi-step macro with Focus Guard and Popup Guard.
`ag-gui maximize [title] [--fullscreen]` | Idempotently maximize or fullscreen window.
`ag-gui focus <title> [--maximize]` | Focus window (with optional auto-maximize).
`ag-gui som-inspect [title]` | Generate `/tmp/ag_som.png` with `[1]`, `[2]` badges and `/tmp/ag_som_map.json`.
`ag-gui click-mark <id>` | Click Set-of-Mark badge ID from cached map.
`ag-gui replace-text "<text>" [--x X --y Y --width 90]` | Safe field replacement across Win32/Wine and Wayland apps.
`ag-gui focused` | Print currently focused window JSON (`title`, `app`, `source`).
`ag-gui find-elements [query] [--window win]` | List visible AT-SPI buttons/inputs/menus as JSON.
`ag-gui click-element "<query>" [--window win]` | Click via AT-SPI first, Smart OCR fallback.
`ag-gui click-text "<query>" [--window win] [--lang eng+ben]` | Dark-mode-aware ranked OCR phrase click.
`ag-gui find-text "<query>" [--screenshot path]` | Ranked OCR bounding-box search.
`ag-gui inspect-window [title]` | Focus, crop, and return AT-SPI + grouped OCR UI labels as JSON.
`ag-gui click <x> <y>` / `click-verify <x> <y>` | Wayland-native kernel `UInput` click (+ optional delta check).
`ag-gui scroll <amount> [--x X --y Y]` | Wayland-native kernel `UInput` wheel scroll.
`ag-gui drag <x1> <y1> <x2> <y2>` | Wayland-native smooth drag-and-drop.
`ag-gui wait-for-text "<query>"` / `wait-for-change` | Pixel-diff-gated deterministic waits.
`ag-gui screenshot [path]` / `screenshot-window [title]` | ~77ms Wayland capture (moves file cleanly, no `/tmp` litter).
`ag-gui copy-image <image_path>` | Wayland clipboard PNG staging.
`ag-gui type "<text>"` / `key <Name>` / `hotkey <mod> <key>` | Stdin-safe typing & normalized XKB combos.
`ag-gui windows` / `display-info` | Active windows JSON / clean `cosmic-randr` output.

---

## 🛡️ Anti-Patterns & Pitfalls

1. **Never send `type`/`key` batches without `guard_window`:** Without Focus Guard, a lost focus dumps keystrokes into background windows or IDE chats.
2. **Never use `Ctrl+A` blindly on Wine/Win32 dialogs (e.g. JHora):** Legacy Win32 `CEdit` ignores `Ctrl+A`; use `replace_text` (mouse drag-select + `BackSpace`) or `Tab` navigation.
3. **Never toggle `Super+m` without checking bounds:** `maximize_window` checks current window dimensions first so already-maximized windows stay maximized.
4. **Never pass raw subshell `/tmp/dbus-*` to `Atspi`:** Always anchor `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$UID/bus` (handled automatically by `ag-gui`).
5. **Never rely on `scrot` / `pyautogui` for Wayland clicks or screenshots:** Use `cosmic-screenshot` + kernel `evdev.UInput`.
