"""Build and visualize the CS 508 Module Seven trie.

PyCharm setup:
1. Open PyCharm's Terminal.
2. Run:  pip install -r requirements.txt
3. Run this file.

Outputs: high-resolution PNG, SVG, PDF, text tree, and node-list CSV.
"""

from pathlib import Path
import csv

PACKAGES_AVAILABLE = True
try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    import networkx as nx
except ImportError:
    PACKAGES_AVAILABLE = False


WORDS = [
    "lark", "car", "lamb", "carb", "lad", "card", "can", "ladle",
    "care", "cared", "label", "coma", "cares", "lard", "carat",
    "laugh", "carp", "cart", "luck", "carry", "lamp", "come", "cane",
    "cone", "calf",
]

OUTPUT_DIR = Path(__file__).parent / "trie_outputs"


class TrieNode:
    """One trie node. Children stores each next letter only once."""

    def __init__(self, node_id, letter="ROOT", prefix=""):
        self.node_id = node_id
        self.letter = letter
        self.prefix = prefix
        self.children = {}
        self.is_word = False


class Trie:
    """A prefix tree that automatically shares common prefixes."""

    def __init__(self):
        self.next_id = 1
        self.root = TrieNode(0)

    def insert(self, word):
        """Insert one word, creating a node only when a prefix is new."""
        current = self.root
        for letter in word.lower().strip():
            if letter not in current.children:
                prefix = current.prefix + letter
                current.children[letter] = TrieNode(self.next_id, letter, prefix)
                self.next_id += 1
            current = current.children[letter]
        current.is_word = True

    def contains(self, word):
        """Return True only if the complete word is stored."""
        current = self.root
        for letter in word.lower():
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.is_word

    def nodes(self):
        """Return every node in preorder."""
        result = []

        def visit(node, depth):
            result.append((node, depth))
            for letter in sorted(node.children):
                visit(node.children[letter], depth + 1)

        visit(self.root, 0)
        return result


def build_trie(words=WORDS):
    """Problem function: create the minimum-node trie for the word list."""
    trie = Trie()
    for word in sorted(set(words)):
        trie.insert(word)
    return trie


def make_networkx_graph(trie):
    """Convert the trie into a NetworkX directed graph."""
    graph = nx.DiGraph()
    for node, depth in trie.nodes():
        graph.add_node(
            node.node_id,
            letter=node.letter,
            prefix=node.prefix,
            is_word=node.is_word,
            depth=depth,
        )
        for child in node.children.values():
            graph.add_edge(node.node_id, child.node_id)
    return graph


def calculate_tree_positions(trie):
    """Give every leaf a slot, then center each parent over its children."""
    positions = {}
    leaf_number = 0

    def place(node, depth):
        nonlocal leaf_number
        if not node.children:
            x = leaf_number
            leaf_number += 1
        else:
            child_x = [place(node.children[key], depth + 1) for key in sorted(node.children)]
            x = sum(child_x) / len(child_x)
        positions[node.node_id] = (x, -depth)
        return x

    place(trie.root, 0)
    return positions


def draw_trie(trie):
    """Create PNG, SVG, and PDF diagrams suitable for a Word document."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    graph = make_networkx_graph(trie)
    positions = calculate_tree_positions(trie)
    leaves = sum(1 for node in graph if graph.out_degree(node) == 0)
    max_depth = max(data["depth"] for _, data in graph.nodes(data=True))
    figure, axis = plt.subplots(figsize=(max(14, leaves * 1.1), max(8, max_depth * 1.6)))
    figure.patch.set_facecolor("white")
    axis.set_facecolor("#f8fafc")

    nx.draw_networkx_edges(
        graph, positions, ax=axis, edge_color="#94a3b8", width=1.8,
        arrows=False, connectionstyle="arc3,rad=0.02"
    )

    for node_id, data in graph.nodes(data=True):
        x, y = positions[node_id]
        is_root = node_id == 0
        is_word = data["is_word"]
        face = "#1d4ed8" if is_root else ("#bbf7d0" if is_word else "#dbeafe")
        edge = "#166534" if is_word else "#1e40af"
        circle = Circle((x, y), 0.29 if not is_root else 0.42,
                        facecolor=face, edgecolor=edge, linewidth=2.2, zorder=3)
        axis.add_patch(circle)
        label = "ROOT" if is_root else data["letter"]
        axis.text(x, y, label, ha="center", va="center", zorder=4,
                  color="white" if is_root else "#172033",
                  fontsize=9 if is_root else 12, fontweight="bold")
        if is_word:
            axis.text(x, y - 0.44, "★ " + data["prefix"], ha="center", va="top",
                      fontsize=8, color="#166534", fontweight="bold")

    axis.set_title("Prefix Tree (Trie) for the Assigned Words", fontsize=21,
                   color="#173f70", fontweight="bold", pad=24)
    axis.text(0.5, 1.01, "Green ★ nodes mark complete words; shared prefixes appear only once.",
              transform=axis.transAxes, ha="center", fontsize=11, color="#475569")
    xs = [x for x, _ in positions.values()]
    axis.set_xlim(min(xs) - 0.8, max(xs) + 0.8)
    axis.set_ylim(-max_depth - 0.8, 0.8)
    axis.set_aspect("equal")
    axis.axis("off")
    figure.tight_layout()

    files = {}
    for extension in ("png", "svg", "pdf"):
        path = OUTPUT_DIR / f"trie_diagram.{extension}"
        figure.savefig(path, dpi=300 if extension == "png" else None,
                       bbox_inches="tight", facecolor=figure.get_facecolor())
        files[extension] = path
    plt.close(figure)
    return files


def draw_svg_without_packages(trie):
    """Always-available SVG fallback if packages have not been installed yet."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    positions = calculate_tree_positions(trie)
    nodes = trie.nodes()
    max_depth = max(depth for _, depth in nodes)
    scale_x, scale_y, margin = 110, 120, 65
    xs = [point[0] for point in positions.values()]
    width = int((max(xs) - min(xs)) * scale_x + 2 * margin)
    height = int(max_depth * scale_y + 2 * margin)

    def point(node_id):
        x, y = positions[node_id]
        return margin + (x - min(xs)) * scale_x, margin - y * scale_y

    svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
           "<rect width='100%' height='100%' fill='#f8fafc'/>"]
    for node, _ in nodes:
        x1, y1 = point(node.node_id)
        for child in node.children.values():
            x2, y2 = point(child.node_id)
            svg.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#94a3b8' stroke-width='3'/>")
    for node, _ in nodes:
        x, y = point(node.node_id)
        root = node.node_id == 0
        fill = '#1d4ed8' if root else ('#bbf7d0' if node.is_word else '#dbeafe')
        radius = 34 if root else 25
        label = 'ROOT' if root else node.letter
        color = 'white' if root else '#172033'
        svg.append(f"<circle cx='{x}' cy='{y}' r='{radius}' fill='{fill}' stroke='#1e40af' stroke-width='3'/>")
        svg.append(f"<text x='{x}' y='{y+5}' text-anchor='middle' font-family='Arial' font-size='{'12' if root else '18'}' font-weight='bold' fill='{color}'>{label}</text>")
        if node.is_word:
            svg.append(f"<text x='{x}' y='{y+45}' text-anchor='middle' font-family='Arial' font-size='12' font-weight='bold' fill='#166534'>★ {node.prefix}</text>")
    svg.append("</svg>")
    path = OUTPUT_DIR / "trie_diagram.svg"
    path.write_text("".join(svg), encoding="utf-8")
    return {"svg": path}


def text_tree(trie):
    """Create a simple text version that can be pasted into notes."""
    lines = ["ROOT"]

    def visit(node, indent):
        children = [node.children[k] for k in sorted(node.children)]
        for index, child in enumerate(children):
            last = index == len(children) - 1
            marker = "└── " if last else "├── "
            word_mark = f"  ★ {child.prefix}" if child.is_word else ""
            lines.append(indent + marker + child.letter + word_mark)
            visit(child, indent + ("    " if last else "│   "))

    visit(trie.root, "")
    return "\n".join(lines)


def export_node_csv(trie):
    """Export proof that every prefix is represented by one node."""
    path = OUTPUT_DIR / "trie_nodes.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Node ID", "Letter", "Prefix", "Complete word?"])
        for node, _ in trie.nodes():
            writer.writerow([node.node_id, node.letter, node.prefix,
                             "Yes" if node.is_word else "No"])
    return path


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    trie = build_trie()
    missing = [word for word in WORDS if not trie.contains(word)]
    if missing:
        raise RuntimeError("Words missing from trie: " + ", ".join(missing))

    tree_text = text_tree(trie)
    text_path = OUTPUT_DIR / "trie_text.txt"
    text_path.write_text(tree_text, encoding="utf-8")
    csv_path = export_node_csv(trie)
    image_files = draw_trie(trie) if PACKAGES_AVAILABLE else draw_svg_without_packages(trie)

    print(tree_text)
    print("\nVerification passed: all", len(set(WORDS)), "words are present.")
    print("Trie nodes including ROOT:", len(trie.nodes()))
    if not PACKAGES_AVAILABLE:
        print("\nSVG created with the built-in fallback.")
        print("For PNG and PDF too, run: pip install networkx matplotlib")
    print("\nFiles created:")
    for path in [*image_files.values(), text_path, csv_path]:
        print(path)


if __name__ == "__main__":
    main()
