# 📊 Obsidian Charts Plugin Reference & Syntax Guide

The **Obsidian Charts** plugin (`phibr0/obsidian-charts`) renders interactive Chart.js visualizations directly from YAML codeblocks or dynamically through DataviewJS.

---

## 1. ⚙️ Basic YAML Codeblock Syntax

Charts are created inside `chart` codeblocks using clean YAML key-value pairs:

```chart
type: bar
labels: [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
series:
  - title: Deep Study Hours
    data: [4.5, 6, 5, 7, 6.5, 8, 3.5]
  - title: Physical Training (min)
    data: [45, 60, 0, 45, 60, 90, 30]
```

---

## 2. 📈 Supported Chart Types & Examples

### A. Line Chart (with Smoothing & Fill)
```chart
type: line
labels: [Week 1, Week 2, Week 3, Week 4, Week 5]
series:
  - title: Mock Test Percentile
    data: [72, 78, 81, 86, 92]
tension: 0.3
fill: true
```

### B. Pie & Doughnut Chart (Distribution & Allocations)
```chart
type: doughnut
labels: [Reasoning & Aptitude, General Science, Current Affairs, English]
series:
  - title: Study Allocation (%)
    data: [35, 30, 20, 15]
options:
  plugins:
    legend:
      position: right
```

### C. Radar Chart (Multi-Dimensional Skill Matrix)
```chart
type: radar
labels: [Speed, Accuracy, Memorization, Conceptual Depth, Endurance]
series:
  - title: Current Assessment
    data: [75, 82, 70, 90, 65]
  - title: Target Benchmark
    data: [90, 95, 85, 95, 85]
```

---

## 3. 🔄 Dynamic DataviewJS Integration

Obsidian Charts exposes a global `window.renderChart()` function, allowing you to dynamically pull YAML properties across hundreds of vault notes and chart them on the fly.

```dataviewjs
const pages = dv.pages('"Daily_Notes"')
  .where(p => p.focus_hours != null)
  .sort(p => p.file.day, 'asc')
  .slice(-14);

const labels = pages.map(p => p.file.day.toISODate()).values;
const data = pages.map(p => p.focus_hours).values;

const chartData = {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      label: 'Focus Hours (Last 14 Days)',
      data: data,
      borderColor: '#38bdf8',
      backgroundColor: 'rgba(56, 189, 248, 0.2)',
      tension: 0.3,
      fill: true
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        max: 12
      }
    }
  }
};

window.renderChart(chartData, this.container);
```
