# 💻 Hardware-Anchored Reality & Display Server Protocol

## 1. The Core Rationale
AI agents frequently operate in serverless, headless cloud containers with unbounded VRAM and ultra-fast NVMe storage. When left unchecked, they generate bloated CSS, excessive animations, and un-paginated UI widgets that choke the user's real-world workstation.

The **Kanad Hardware-Anchored Protocol** anchors all aesthetic and architectural choices directly into the user's physical hardware constraints.

---

## 2. Standard Machine Profile: Dell Inspiron 15-3567 Benchmark

| Subsystem | Physical Specification | Engineering Limit / Constraint |
| :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i3-6006U (2C/4T @ 2.00 GHz, 3MB Cache) | Max 2 simultaneous intensive threads. Heavy Python regex or Dataview queries must be scoped. |
| **Graphics (iGPU)** | Intel HD Graphics 520 (Skylake GT2, 24 EUs) | Low pixel fill-rate. **Zero GPU backdrop blurring**. |
| **Memory (RAM)** | 8GB DDR4 + 7.6GB ZRAM Swap | Prevent Electron memory leaks. Limit simultaneous subagent processes. |
| **Display Server** | Pop!_OS 24.04 LTS (COSMIC Wayland Compositor) | Electron/Chromium Wayland surface buffer synchronization. |
| **Display Resolution** | 15.6" Full HD (1920x1080) | `baseFontSize: 20` requires wide table scroll containers. |

---

## 3. The 4 Strict GPU & Rendering Guardrails

### 3.1 Strict Prohibition of `backdrop-filter: blur()`
- **The Failure Mode:** `backdrop-filter: blur(12px)` requires the GPU to copy the current framebuffer into an intermediate texture, perform multi-pass Gaussian blur passes, and composite it back onto the display surface on every scroll event.
- **The Consequence on Intel HD 520:** Drops window scrolling from 60fps to 12-15fps with severe Wayland compositor micro-stutters.
- **The Mandated Alternative:** Solid dark surfaces with alpha opacity:
  ```css
  /* ❌ FORBIDDEN */
  .dashboard-card {
    background: rgba(28, 32, 42, 0.65);
    backdrop-filter: blur(16px);
  }

  /* ✅ MANDATED (GPU-Safe 60fps) */
  .dashboard-card {
    background: #1c202a;
    border: 1px solid #323946;
    transform: translateY(-2px); /* Pure transform, no blur */
    transition: transform 0.15s ease, border-color 0.15s ease;
  }
  ```

### 3.2 20px Typographic Scaling & Horizontal Clipping
- At `baseFontSize: 20`, large KaTeX equations, chemical formulas, and multi-column tables will exceed standard viewport widths.
- All technical cards and formula guides must include:
  ```css
  .math-block, .table-view-table {
    overflow-x: auto;
    max-width: 100%;
  }
  ```

### 3.3 Scoped Dataview Queries (CPU Cycle Protection)
- Unbounded Dataview queries parse every markdown file in the vault on load.
- Mandatory pattern:
  ```dataview
  TABLE WITHOUT ID file.link AS "Note", file.folder AS "Module"
  FROM "Polity ⚖️"
  WHERE file.name != "Polity ⚖️"
  SORT file.mtime DESC
  LIMIT 8
  ```

### 3.4 Hardware Profiling Shell Routine
Agents must run the following check before recommending heavy visual changes:
```bash
# Check CPU, GPU and Wayland status
lscpu | grep "Model name"
lspci | grep -i vga
echo $XDG_SESSION_TYPE
```