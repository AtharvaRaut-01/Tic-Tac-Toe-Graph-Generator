# 📌 Tic-Tac-Toe Interactive State-Space Tree (HTML Visualization)

This project generates a fully **interactive, zoomable Tic-Tac-Toe game tree** using pure **HTML + JavaScript (vis.js)** — no external servers, no frameworks, no dependencies except Python.

You can explore the entire decision space of Tic-Tac-Toe:

* Zoom & pan across the game tree
* View mini tic-tac-toe boards as nodes
* Click any node to see a large preview
* Inspect board metadata (winner, status, level, board string)
* Copy board strings
* Move nodes manually
* Reset & auto-fit the view

This tool is perfect for **AI search visualization**, **Minimax demonstration**, **game-theory learning**, and helping beginners explore how games branch.

---

## 🚀 Features

### ✔ Fully interactive HTML (no installation required)

Open `ttt_tree_interactive.html` in any browser.

### ✔ Mini-boards rendered as SVG

Clean, crisp visuals that scale without pixelation.

### ✔ Click a node → see full board preview

Shows full board, winner status, depth, and more.

### ✔ Adjustable depth

Choose how many levels of the game tree to generate (recommended: 2–4).

### ✔ Lightweight & standalone

Everything runs offline.
All assets are embedded directly in the HTML file.

---

## 📂 Project Structure

```
.
├── ttt_interactive_standalone.py   # main generator script
└── ttt_tree_interactive.html       # output (auto-generated)
```

---

## 🛠 Requirements

Python 3.8+
No external libraries required — uses only standard library.

---

## 🔧 Usage

### 1️⃣ Set the depth

Open `ttt_interactive_standalone.py` and edit:

```python
MAX_LEVEL = 3
```

Recommended values:

* `2` → root + X moves
* `3` → root + X + O replies
* `4` → deeper expansion (much bigger tree)

Maximum allowed is capped for performance.

---

### 2️⃣ Run the generator

```bash
python ttt_interactive_standalone.py
```

This creates:

```
ttt_tree_interactive.html
```

---

### 3️⃣ Open the visualization

Just double-click the HTML file.
No server needed. Works offline.

---

## 🎮 Controls

| Action           | How                           |
| ---------------- | ----------------------------- |
| Zoom in          | Mouse wheel / Zoom In button  |
| Zoom out         | Mouse wheel / Zoom Out button |
| Drag             | Hold left mouse button        |
| Reset layout     | Reset button                  |
| Fit to screen    | Fit button                    |
| See node details | Click any node                |

---

## 🧠 How It Works

* Board states are generated via BFS up to a chosen depth.
* Each board is transformed into an SVG.
* SVGs are embedded as base64 images in nodes.
* Nodes and edges are encoded into JSON.
* A standalone HTML file is generated using **vis.js** for interaction.

---

## ⭐ Example Output

The visualization looks like a branching tree with:

* The empty board at the top
* All possible moves expanding downward
* Clean mini-board icons
* Smooth edges and arrows

Clicking any board opens a right-side details panel.

---

## 📜 License

This project is open-source and free to use.
Feel free to modify, expand, or integrate into your AI/game-theory projects.

