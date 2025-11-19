"""
ttt_interactive_standalone.py

Generates ttt_tree_interactive.html: an interactive, zoomable, hierarchical
game-tree visualization for Tic-Tac-Toe using vis.js (no pyvis/Jinja2 required).

Now UPDATED with:
✔ Runtime depth selection (asks user in terminal)
✔ Input clamped to safety range (1–5)
"""

import json
import base64
from collections import deque, defaultdict
import os

# -----------------------
# ASK USER FOR DEPTH
# -----------------------
def get_depth_from_user():
    print("Select depth of Tic-Tac-Toe game tree")
    print("(Recommended: 2–4. Maximum allowed: 5)\n")
    while True:
        try:
            d = int(input("Enter tree depth (1–5): ").strip())
            if 1 <= d <= 5:
                return d
            else:
                print("❌ Please enter a valid number between 1 and 5.")
        except:
            print("❌ Invalid input. Enter a number 1–5.")

MAX_LEVEL = get_depth_from_user()
CAP_LEVEL = 5
if MAX_LEVEL > CAP_LEVEL:
    MAX_LEVEL = CAP_LEVEL

print(f"\nUsing MAX_LEVEL = {MAX_LEVEL}\n")

# -----------------------
# OUTPUT SETTINGS
# -----------------------
OUT_HTML = "ttt_tree_interactive.html"
SVG_SMALL = (96, 96)     # small icon on node
SVG_LARGE = (260, 260)   # preview in details panel

# -----------------------
# Tic-Tac-Toe logic
# -----------------------
WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def check_win(board, p):
    return any(all(board[i] == p for i in line) for line in WIN_LINES)

def winner_of(board):
    if check_win(board, "X"):
        return "X"
    if check_win(board, "O"):
        return "O"
    if "." not in board:
        return "Draw"
    return None

def is_terminal(board):
    return winner_of(board) is not None

def next_player(board):
    X = board.count("X")
    O = board.count("O")
    return "X" if X == O else "O"

def generate_children(board):
    if is_terminal(board):
        return []
    p = next_player(board)
    children = []
    for i in range(9):
        if board[i] == ".":
            nb = board[:i] + p + board[i+1:]
            # impossible state prune
            if not (check_win(nb, "X") and check_win(nb, "O")):
                children.append(nb)
    return children

# -----------------------
# Build limited-depth tree (BFS)
# -----------------------
def build_limited_tree(max_level):
    root = "........."
    G_edges = []
    level_of = {root: 0}
    nodes_by_level = defaultdict(list)
    nodes_by_level[0].append(root)
    q = deque([root])

    while q:
        b = q.popleft()
        lvl = level_of[b]
        if lvl >= max_level - 1:
            continue
        for c in generate_children(b):
            G_edges.append((b, c))
            if c not in level_of:
                level_of[c] = lvl + 1
                nodes_by_level[lvl+1].append(c)
                q.append(c)

    all_nodes = list(level_of.keys())
    return all_nodes, G_edges, level_of

# -----------------------
# SVG Generator
# -----------------------
def board_to_svg(board, width=96, height=96, x_color="#d72638", o_color="#3a86ff", stroke="#1b1b1b"):
    cell_w = width / 3.0
    cell_h = height / 3.0
    line_w = max(1.0, width * 0.03)

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg_parts.append(f'<rect width="{width}" height="{height}" rx="8" ry="8" fill="#ffffff"/>')

    # grid lines
    for i in range(1,3):
        x = i * cell_w
        y = i * cell_h
        svg_parts.append(f'<line x1="{x:.2f}" y1="0" x2="{x:.2f}" y2="{height}" stroke="{stroke}" stroke-width="{line_w*0.45}" />')
        svg_parts.append(f'<line x1="0" y1="{y:.2f}" x2="{width}" y2="{y:.2f}" stroke="{stroke}" stroke-width="{line_w*0.45}" />')

    # symbols
    for idx, c in enumerate(board):
        if c == '.':
            continue
        r = idx // 3
        col = idx % 3
        cx = col * cell_w + cell_w/2
        cy = r * cell_h + cell_h/2
        if c == 'X':
            pad = min(cell_w, cell_h) * 0.28
            x1 = cx - (cell_w/2 - pad); y1 = cy - (cell_h/2 - pad)
            x2 = cx + (cell_w/2 - pad); y2 = cy + (cell_h/2 - pad)
            x3 = cx - (cell_w/2 - pad); y3 = cy + (cell_h/2 - pad)
            x4 = cx + (cell_w/2 - pad); y4 = cy - (cell_h/2 - pad)
            svg_parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{x_color}" stroke-width="{max(2, line_w)}"/>')
            svg_parts.append(f'<line x1="{x3:.2f}" y1="{y3:.2f}" x2="{x4:.2f}" y2="{y4:.2f}" stroke="{x_color}" stroke-width="{max(2, line_w)}"/>')
        else:
            r2 = min(cell_w, cell_h) * 0.28
            svg_parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r2:.2f}" fill="none" stroke="{o_color}" stroke-width="{max(2, line_w)}" />')

    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def svg_to_data_url(svg):
    b = svg.encode('utf-8')
    return "data:image/svg+xml;base64," + base64.b64encode(b).decode()

# -----------------------
# Build JSON for vis.js
# -----------------------
def make_vis_data(nodes, edges, level_of):
    nodes_json = []
    edges_json = []

    nodes_sorted = sorted(nodes, key=lambda n: (level_of[n], n))

    for nid in nodes_sorted:
        lvl = level_of[nid]
        small = svg_to_data_url(board_to_svg(nid, SVG_SMALL[0], SVG_SMALL[1]))
        large = svg_to_data_url(board_to_svg(nid, SVG_LARGE[0], SVG_LARGE[1]))

        w = winner_of(nid)
        status = "terminal" if w else "ongoing"

        nodes_json.append({
            "id": nid,
            "label": "",
            "shape": "image",
            "image": small,
            "title": f"<b>Level:</b> {lvl}<br><b>Status:</b> {status}<br><b>Winner:</b> {w or '-'}",
            "level": lvl,
            "data": {
                "board": nid,
                "level": lvl,
                "status": status,
                "winner": w or "",
                "large_svg": large
            }
        })

    for a, b in edges:
        edges_json.append({"from": a, "to": b})

    return nodes_json, edges_json

# -----------------------
# HTML Template (vis.js)
# -----------------------
HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Tic-Tac-Toe Tree</title>
<script src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
<style>
body { margin:0; display:flex; height:100vh; font-family:Arial; }
#network { flex:1; }
#panel { width:340px; border-left:1px solid #ddd; padding:12px; overflow:auto; }
</style>
</head>
<body>
<div id="network"></div>
<div id="panel">
<h3>Node Details</h3>
<div id="node_details">Click a node.</div>
</div>

<script>
const nodes_data = __NODES_JSON__;
const edges_data = __EDGES_JSON__;

const nodes = new vis.DataSet(nodes_data.map(n=>{
    const o = {id:n.id, shape:n.shape, image:n.image, title:n.title, level:n.level};
    o._data = n.data;
    return o;
}));
const edges = new vis.DataSet(edges_data);

const network = new vis.Network(
    document.getElementById('network'),
    {nodes, edges},
    {
        layout:{ hierarchical:{enabled:true, direction:"UD", levelSeparation:150} },
        interaction:{hover:true},
        physics:false
    }
);

network.on("click", function(p){
    if (!p.nodes.length) return;
    const nid = p.nodes[0];
    const nd = nodes.get(nid)._data;
    document.getElementById("node_details").innerHTML =
        `<img src="${nd.large_svg}" style="width:260px"><br><br>
         <b>Board:</b><pre>${nd.board}</pre>
         <b>Level:</b> ${nd.level}<br>
         <b>Status:</b> ${nd.status}<br>
         <b>Winner:</b> ${nd.winner || "-"}`;
});
</script>
</body></html>
"""

# -----------------------
# Main script
# -----------------------
def main():
    nodes, edges, level_of = build_limited_tree(MAX_LEVEL)
    print(f"Built tree: {len(nodes)} nodes, {len(edges)} edges")

    nodes_json, edges_json = make_vis_data(nodes, edges, level_of)

    html = HTML_TEMPLATE.replace("__NODES_JSON__", json.dumps(nodes_json))
    html = html.replace("__EDGES_JSON__", json.dumps(edges_json))

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nGenerated: {OUT_HTML}")
    print("Open it in your browser to explore the interactive tree.")

if __name__ == "__main__":
    main()
