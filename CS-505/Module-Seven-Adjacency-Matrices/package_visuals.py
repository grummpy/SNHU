"""Optional package-powered visuals for adjacency_matrix_pycharm.py."""

from pathlib import Path


def create_matrix_package_visuals(data, output_folder: Path):
    """Create heatmaps, a NetworkX path graph, and an eigenvector plot."""
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        import numpy as np
        import seaborn as sns
    except ImportError:
        print("\nOptional charts skipped. Install them with:")
        print("pip install -r requirements.txt")
        return []

    files = []
    output_folder.mkdir(exist_ok=True)

    # Heatmaps make adjacency and numerical matrices easier to read.
    a1, a2, a3, r1, r2 = data["relations"]
    heatmaps = [
        ("relation_r1_heatmap", r1, a2, a1, "R1 adjacency matrix"),
        ("relation_r2_heatmap", r2, a3, a2, "R2 adjacency matrix"),
        ("matrix_product_heatmap", data["product"], ["Col 1", "Col 2"],
         ["Row 1", "Row 2"], "Matrix product A × B"),
        ("inverse_heatmap", data["inverse"], ["1", "2", "3"],
         ["1", "2", "3"], "Inverse of A"),
    ]
    for filename, matrix, columns, rows, title in heatmaps:
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        sns.heatmap(np.array(matrix, dtype=float), annot=True, fmt=".4g",
                    cmap="Blues", linewidths=1, cbar=True,
                    xticklabels=columns, yticklabels=rows, ax=ax)
        ax.set_title(title, color="#173f70", fontsize=15, fontweight="bold")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
        fig.tight_layout()
        path = output_folder / f"{filename}.png"
        fig.savefig(path, dpi=220, bbox_inches="tight")
        plt.close(fig)
        files.append(path)

    # NetworkX draws the weighted graph and highlights the shortest path.
    graph = nx.Graph()
    matrix, labels = data["weighted_graph"], data["graph_labels"]
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] > 0:
                graph.add_edge(labels[i], labels[j], weight=matrix[i][j])
    chosen = list(zip(data["path_labels"], data["path_labels"][1:]))
    pos = nx.spring_layout(graph, seed=505)
    edge_colors = ["#dc2626" if (u, v) in chosen or (v, u) in chosen else "#94a3b8"
                   for u, v in graph.edges()]
    widths = [4 if color == "#dc2626" else 2 for color in edge_colors]
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="#dbeafe", node_size=1800,
            edge_color=edge_colors, width=widths, font_weight="bold", ax=ax)
    nx.draw_networkx_edge_labels(graph, pos,
                                 edge_labels=nx.get_edge_attributes(graph, "weight"), ax=ax)
    ax.set_title("Dijkstra Shortest Path (red)", fontsize=16,
                 color="#173f70", fontweight="bold")
    ax.axis("off")
    path = output_folder / "shortest_path_networkx.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    files.append(path)

    # Show the two eigenvector directions.
    eigenvalues, eigenvectors = data["eigen"]
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ["#2563eb", "#dc2626"]
    for value, vector, color in zip(eigenvalues, eigenvectors, colors):
        ax.quiver(0, 0, vector[0], vector[1], angles="xy", scale_units="xy",
                  scale=1, color=color, width=0.015, label=f"λ = {value:g}")
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color="#cbd5e1"); ax.axvline(0, color="#cbd5e1")
    ax.set_aspect("equal"); ax.grid(alpha=.25); ax.legend()
    ax.set_title("Eigenvector Directions", fontsize=16, color="#173f70", fontweight="bold")
    path = output_folder / "eigenvectors.png"
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    files.append(path)
    print(f"\nPackage visuals created: {len(files)} PNG charts")
    return files
