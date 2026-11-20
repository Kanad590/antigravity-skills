---
name: desktop-gui-control
description: >-
  Use this skill whenever the user asks to automate, control, click, type, or interact with desktop GUI applications on Pop!_OS (COSMIC Wayland or Xwayland),
  including Tuta Mail, JHora (Jagannatha Hora in Wine), browsers, terminal windows, media players, or native system apps.
  Provides Wayland-native input simulation (wtype, ydotool evdev), zero-hang screenshotting (cosmic-screenshot),
  deterministic keyboard form navigation, and OCR/visual-diff verification.
---

# Desktop GUI Control & Automation Skill (Pop!_OS COSMIC Wayland)

This skill provides indestructible, deterministic desktop GUI automation, mouse/keyboard control, and visual verification for applications running on Pop!_OS 24.04 LTS (COSMIC Desktop, Wayland session `wayland-1`, physical display `1366×768`).

---

## 🖥️ System Architecture & Protocols

Property | Configuration
:--- | :---
**OS / Desktop** | Pop!_OS 24.04 LTS (COSMIC Desktop / `cosmic-comp`)
**Display Environment** | `WAYLAND_DISPLAY=wayland-1`, `DISPLAY=:1`
**Screenshots** | `cosmic-screenshot --interactive=false --notify=false -s /tmp` (Wayland native, 0% hang)
**Keyboard Emulation** | `/usr/bin/wtype` via Wayland `virtual-keyboard-v1` protocol
**Hardware Input Daemon**| `/usr/bin/ydotoold` running in user systemd (`ydotoold.service`)
**CLI Automation Hub** | `ag-gui` (`~/.local/bin/ag-gui` and `/usr/local/bin/ag-gui`)
**FastMCP Server** | `linux-desktop-apps-mcp` (27 tools registered)

---

## ⚡ Core CLI Commands (`ag-gui`)

Command | Description
:--- | :---
`ag-gui screenshot [path]` | Instant full-screen capture via `cosmic-screenshot`.
`ag-gui screenshot-window [title] [--output path]` | Crops screenshot strictly to target window bounds, rejecting phantom headless windows.
`ag-gui inspect-window [title]` | Focuses window, crops screenshot, extracts all visible text/buttons as JSON metadata.
`ag-gui overlay-grid <image> [--output path]` | Overlays high-contrast alphanumeric coordinate grid (`A1..Z10`) at ~23 KB.
`ag-gui click-verify <x> <y> [--button left]` | Dispatches click with 0.63ms visual delta verification to confirm UI changed.
`ag-gui click-text "<query>" [--window <win>]` | Locates text/phrase via multi-word OCR and clicks exact center.
`ag-gui find-text "<query>" [--screenshot <path>]` | Sliding-window multi-word OCR (supports `eng+ben`) with bounding boxes.
`ag-gui drag <x1> <y1> <x2> <y2> [--duration 0.4]` | Smooth hardware mouse drag-and-drop between coordinates.
`ag-gui wait-for-text "<query>" [--timeout 10]` | Deterministically waits for text to appear on screen/window, avoiding race conditions.
`ag-gui copy-image <image_path>` | Stages local image into Wayland clipboard (`image/png`) with pipe isolation (0% hang).
`ag-gui display-info` | Returns native resolution, scaling, and modes from `cosmic-randr list`.
`ag-gui focus <title>` | 3-Layer hybrid focus: Xwayland wmctrl + Safe Titlebar Center click (`x+w//2, y+15`).
`ag-gui type "<text>" [--delay 0.02]` | Types text with configurable inter-key delay.
`ag-gui key <KeyName>` | Presses single named key (`Tab`, `Return`, `Escape`, `F1`, `Down`, `Up`, `space`).
`ag-gui hotkey <mod> <key>` | Simulates shortcut on Wayland (e.g. `ctrl n`, `alt f4`).

---

## 🛠️ FastMCP High-Level Tools (`linux-desktop-apps`)

Tool | Parameters | Description
:--- | :--- | :---
`gui_smart_click` | `target`, `window=None`, `button="left"`, `double=False` | Universal clicker: coordinates (`"500, 300"`) or multi-word phrase (`"New Conversation"`).
`gui_inspect_window` | `window_title=None` | Crops active window, extracts all visible text elements with center coordinates.
`gui_visual_grid_inspect` | `window_title=None` | Overlays coordinate grid (`A1..D8`) on target window for unknown canvas or icon apps.
`gui_drag_and_drop` | `start_x`, `start_y`, `end_x`, `end_y`, `duration=0.5` | Smooth hardware drag-and-drop.
`gui_wait_for` | `text=None`, `window_title=None`, `timeout=10` | Deterministic state wait helper.
`gui_copy_image_to_clipboard`| `image_path` | Stages image to system clipboard for instant `Ctrl+V` pasting.
`gui_get_display_info` | *none* | Returns display resolution, refresh rate, and scaling factor.

---

## 🔮 Unknown Application Workflow (Visual Grounding)

When interacting with a completely unknown or custom application:
1. **Target & Inspect:** Call `gui_inspect_window("AppName")`. If text buttons are present, click by label via `gui_smart_click("Save")`.
2. **Icon / Canvas Inspection:** If the app has no text, call `gui_visual_grid_inspect("AppName")`. The tool returns an annotated screenshot with alphanumeric grid boxes (`A1..D8`).
3. **Execute & Verify:** Click the desired cell center via `gui_smart_click("x, y")`. The tool computes visual delta to confirm the UI responded.

---

## 📧 Application Recipes: Tuta Mail Flatpak Automation

Tuta Mail (`com.tutanota.Tutanota`) runs natively on Wayland (`--ozone-platform=wayland`).

### 1. Launching & Bringing to Front
```bash
flatpak run com.tutanota.Tutanota &
ag-gui focus "Tutanota"
```

### 2. Form Navigation & Image Pasting
- **New Email:** `ag-gui hotkey ctrl n`
- **Fill Recipient:** `ag-gui type "email@example.com" --delay 0.02` then `ag-gui key Return`
- **Attach/Paste Generated Chart:**
  ```bash
  ag-gui copy-image /path/to/chart.png
  ag-gui hotkey ctrl v
  ```
- **Send:** `ag-gui click-text "Send"` or `Tab` cycle to `Send` + `Return`.

---

## 🔮 Application Recipes: Jagannatha Hora (JHora Wine)

JHora runs under Wine using Xwayland.

1. **Launch:** `wine ~/.wine/drive_c/jhora/jhora.exe &`
2. **Bring to Front:** `ag-gui focus "Jagannatha Hora"` (uses `wmctrl -a`).
3. **Menu Access:** Use `Alt` accelerators via `wtype` (e.g. `ag-gui hotkey alt v`).
4. **Targeted Chart Capture:**
   `ag-gui screenshot-window "Jagannatha Hora" --output /tmp/jhora_chart.png`

---

## 🛡️ Anti-Patterns & Pitfalls

1. **Never parse `cosmic-screenshot` from directory glob races:** Parse the exact path outputted to `stdout`.
2. **Never invoke `wl-copy` in Python without `DEVNULL`:** Subprocesses hang waiting for pipe EOF because `wl-copy` daemonizes itself. Always use `stdout=DEVNULL, stderr=DEVNULL`.
3. **Never click at `x=30, y=10` to focus browser windows:** It hits tab close buttons. Use titlebar center `(ext.x + ext.width // 2, ext.y + 15)`.
4. **Never query child AT-SPI widgets on Electron/Chrome:** They return `None`. Use Tesseract Word-Box OCR on the window crop instead.
