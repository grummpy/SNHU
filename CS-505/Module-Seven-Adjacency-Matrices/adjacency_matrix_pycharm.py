"""CS 505 Module Seven: Adjacency Matrix activity.

Run this file in PyCharm. It uses only Python's standard library and creates
an HTML report plus CSV files in the matrix_outputs folder.
"""

from __future__ import annotations

import csv
import heapq
import html
import math
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "matrix_outputs"


def format_matrix(matrix, decimals=4):
    """Return a matrix as aligned text."""
    return "\n".join("[ " + "  ".join(f"{v:.{decimals}g}" if isinstance(v, float) else str(v) for v in row) + " ]" for row in matrix)


def save_csv(filename, matrix, row_labels=None, col_labels=None):
    """Save a matrix or table so it can be opened in Excel."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if col_labels is not None:
            writer.writerow(([""] if row_labels is not None else []) + list(col_labels))
        for i, row in enumerate(matrix):
            writer.writerow(([row_labels[i]] if row_labels is not None else []) + list(row))


def problem_1_relation_matrices():
    """Build the adjacency matrix for each relation directly from its rule."""
    a1, a2, a3 = [3, 8, 4, 6], [6, 8, 7], [1, 2, 3]

    def relation_matrix(domain, codomain, rule):
        return [[1 if rule(x, y) else 0 for y in codomain] for x in domain]

    r1 = relation_matrix(a1, a2, lambda x, y: y - x == 2)
    r2 = relation_matrix(a2, a3, lambda x, y: y - x == 1)
    save_csv("problem_1_r1.csv", r1, a1, a2)
    save_csv("problem_1_r2.csv", r2, a2, a3)
    return a1, a2, a3, r1, r2


def problem_2_shortest_path(adjacency_matrix, start, end):
    """Dijkstra's algorithm for a weighted adjacency matrix; 0 means no edge."""
    n = len(adjacency_matrix)
    distance = [math.inf] * n
    previous = [None] * n
    distance[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current_distance != distance[current]:
            continue
        if current == end:
            break
        for neighbor, weight in enumerate(adjacency_matrix[current]):
            if weight > 0:
                new_distance = current_distance + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(queue, (new_distance, neighbor))

    if math.isinf(distance[end]):
        return math.inf, []
    path, node = [], end
    while node is not None:
        path.append(node)
        node = previous[node]
    return distance[end], list(reversed(path))


def problem_3_complexity_table():
    """Complexities when a graph is stored as a V by V adjacency matrix."""
    return [
        ["Check whether one edge exists", "O(1)", "O(V²)", "One matrix cell is checked."],
        ["List all neighbors of one vertex", "O(V)", "O(V²)", "Scan one complete row."],
        ["Breadth-first search (BFS)", "O(V²)", "O(V²)", "Each visited vertex scans a row."],
        ["Depth-first search (DFS)", "O(V²)", "O(V²)", "Each visited vertex scans a row."],
        ["Dijkstra shortest path", "O(V²)", "O(V²)", "Basic matrix version scans vertices and rows."],
        ["Prim minimum spanning tree", "O(V²)", "O(V²)", "Basic matrix version repeatedly scans vertices."],
        ["Floyd-Warshall all-pairs paths", "O(V³)", "O(V²)", "Three nested loops update the matrix."],
    ]


def problem_4_can_add(a, b):
    """Matrices can be added only when their row and column counts match."""
    shape_a = (len(a), len(a[0]))
    shape_b = (len(b), len(b[0]))
    if shape_a != shape_b:
        return False, None, f"No. A is {shape_a[0]}×{shape_a[1]} and B is {shape_b[0]}×{shape_b[1]}."
    result = [[a[r][c] + b[r][c] for c in range(shape_a[1])] for r in range(shape_a[0])]
    return True, result, "Yes. The matrices have the same dimensions."


def problem_5_can_multiply(a, b):
    """A×B is possible when A's columns equal B's rows."""
    possible = len(a[0]) == len(b)
    explanation = (f"Yes. A has {len(a[0])} columns and B has {len(b)} rows. "
                   f"The result will be {len(a)}×{len(b[0])}.") if possible else "No. The inner dimensions do not match."
    return possible, explanation


def problem_6_multiply(a, b):
    """Multiply matrices using row-by-column dot products."""
    if len(a[0]) != len(b):
        raise ValueError("The inner matrix dimensions must match.")
    return [[sum(a[r][k] * b[k][c] for k in range(len(b))) for c in range(len(b[0]))] for r in range(len(a))]


def problem_7_solve_linear_system(coefficients, answers):
    """Solve Ax=b with Gauss-Jordan elimination."""
    n = len(coefficients)
    augmented = [list(map(float, coefficients[i])) + [float(answers[i])] for i in range(n)]
    steps = []
    for column in range(n):
        pivot = max(range(column, n), key=lambda r: abs(augmented[r][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("The system does not have one unique solution.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [v / pivot_value for v in augmented[column]]
        for row in range(n):
            if row != column:
                factor = augmented[row][column]
                augmented[row] = [augmented[row][c] - factor * augmented[column][c] for c in range(n + 1)]
        steps.append([row[:] for row in augmented])
    return [round(augmented[i][-1], 10) for i in range(n)], steps


def problem_8_graph_explanation():
    return ("An adjacency matrix uses one row and one column for every vertex. A 1 means two vertices "
            "are connected and a 0 means they are not. In a weighted graph, the cell stores the edge's "
            "weight instead of 1. An undirected graph produces a matrix mirrored across its diagonal.")


def problem_9_computer_science_uses():
    return ("Computers use matrix operations for graph paths, image transformations, 3D graphics, machine "
            "learning, and network analysis. For example, powers of an adjacency matrix can count walks "
            "between vertices, while matrix multiplication combines transformations or layers of data.")


def determinant_3x3(a):
    """Find a 3×3 determinant by cofactor expansion."""
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def problem_10_determinant(a):
    return determinant_3x3(a)


def problem_11_inverse(a):
    """Find an inverse by Gauss-Jordan elimination on [A | I]."""
    n = len(a)
    work = [[float(a[r][c]) for c in range(n)] + [1.0 if r == c else 0.0 for c in range(n)] for r in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(work[r][col]))
        if abs(work[pivot][col]) < 1e-12:
            raise ValueError("This matrix has no inverse.")
        work[col], work[pivot] = work[pivot], work[col]
        p = work[col][col]
        work[col] = [v / p for v in work[col]]
        for r in range(n):
            if r != col:
                factor = work[r][col]
                work[r] = [work[r][c] - factor * work[col][c] for c in range(2 * n)]
    return [[round(work[r][n + c], 10) for c in range(n)] for r in range(n)]


def problem_12_eigen_2x2(a):
    """Find eigenvalues/eigenvectors of a symmetric 2×2 matrix."""
    p, q = a[0]
    r, s = a[1]
    trace, det = p + s, p * s - q * r
    root = math.sqrt(trace * trace - 4 * det)
    values = [(trace + root) / 2, (trace - root) / 2]
    vectors = []
    for value in values:
        vector = (q, value - p) if abs(q) > 1e-12 else (value - s, r)
        length = math.hypot(*vector)
        vectors.append(tuple(round(v / length, 6) for v in vector))
    return values, vectors


def matrix_html(title, matrix, row_labels=None, col_labels=None):
    out = [f"<h3>{html.escape(title)}</h3><table class='matrix'>"]
    if col_labels is not None:
        out.append("<tr>" + ("<th></th>" if row_labels else "") + "".join(f"<th>{x}</th>" for x in col_labels) + "</tr>")
    for i, row in enumerate(matrix):
        out.append("<tr>" + (f"<th>{row_labels[i]}</th>" if row_labels else "") + "".join(f"<td class='v{int(v) if v in (0,1) else 2}'>{v:g}</td>" if isinstance(v, (int,float)) else f"<td>{html.escape(str(v))}</td>" for v in row) + "</tr>")
    return "".join(out) + "</table>"


def graph_svg(matrix, labels, path=None):
    """Draw a small circular graph; shortest-path edges are red."""
    n, cx, cy, radius = len(labels), 310, 190, 130
    points = [(cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    path_edges = {tuple(sorted((path[i], path[i+1]))) for i in range(len(path or []) - 1)}
    parts = ["<svg viewBox='0 0 620 380' class='diagram'>", "<defs><marker id='arrow' markerWidth='8' markerHeight='8' refX='7' refY='4' orient='auto'><path d='M0,0 L8,4 L0,8 z' fill='#64748b'/></marker></defs>"]
    for i in range(n):
        for j in range(i + 1, n):
            weight = matrix[i][j] or matrix[j][i]
            if weight:
                chosen = (i, j) in path_edges
                color, width = ("#dc2626", 5) if chosen else ("#94a3b8", 2)
                x1,y1=points[i]; x2,y2=points[j]
                parts.append(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' stroke-width='{width}'/>")
                parts.append(f"<text x='{(x1+x2)/2:.1f}' y='{(y1+y2)/2-5:.1f}' class='weight'>{weight}</text>")
    for i,(x,y) in enumerate(points):
        fill = "#fee2e2" if path and i in path else "#dbeafe"
        parts.extend([f"<circle cx='{x:.1f}' cy='{y:.1f}' r='25' fill='{fill}' stroke='#1e3a8a' stroke-width='2'/>", f"<text x='{x:.1f}' y='{y+5:.1f}' class='node'>{html.escape(str(labels[i]))}</text>"])
    return "".join(parts) + "</svg>"


def relation_svg(domain, codomain, matrix, title):
    h = max(len(domain), len(codomain)) * 65 + 45
    parts = [f"<h3>{title}</h3><svg viewBox='0 0 620 {h}' class='diagram'>", "<defs><marker id='relArrow' markerWidth='8' markerHeight='8' refX='7' refY='4' orient='auto'><path d='M0,0 L8,4 L0,8 z' fill='#2563eb'/></marker></defs>"]
    for i,x in enumerate(domain):
        y1=45+i*65
        for j,_ in enumerate(codomain):
            if matrix[i][j]:
                y2=45+j*65
                parts.append(f"<line x1='205' y1='{y1}' x2='415' y2='{y2}' stroke='#2563eb' stroke-width='3' marker-end='url(#relArrow)'/>")
    for x,col,side in ((domain,170,'start'),(codomain,450,'end')):
        for i,v in enumerate(x):
            y=45+i*65
            parts.append(f"<circle cx='{col}' cy='{y}' r='23' fill='#eff6ff' stroke='#1d4ed8' stroke-width='2'/><text x='{col}' y='{y+5}' class='node'>{v}</text>")
    return "".join(parts)+"</svg>"


def create_report(data):
    a1,a2,a3,r1,r2=data["relations"]
    a,b=data["a"],data["b"]
    solution=data["solution"]
    eigvals,eigvecs=data["eigen"]
    comp_rows="".join("<tr>"+"".join(f"<td>{html.escape(str(v))}</td>" for v in row)+"</tr>" for row in data["complexities"])
    report=f"""<!doctype html><html><head><meta charset='utf-8'><title>Adjacency Matrix Activity</title>
<style>body{{font-family:Arial,sans-serif;max-width:1050px;margin:35px auto;padding:0 25px;color:#172033;background:#f8fafc}}h1{{color:#173f70}}h2{{margin-top:38px;color:#1d4ed8;border-bottom:2px solid #bfdbfe;padding-bottom:6px}}h3{{margin-bottom:8px}}.card{{background:white;padding:22px;margin:18px 0;border-radius:12px;box-shadow:0 2px 12px #dbe4ef}}table{{border-collapse:collapse;width:100%;margin:12px 0}}th,td{{border:1px solid #cbd5e1;padding:9px;text-align:center}}th{{background:#dbeafe}}.matrix{{width:auto}}.matrix td{{min-width:42px;font-weight:bold}}.v1{{background:#bbf7d0}}.v0{{background:#f1f5f9;color:#64748b}}code,pre{{background:#eff6ff;padding:10px;border-radius:7px;white-space:pre-wrap}}.diagram{{width:100%;max-height:430px;background:#fff;border:1px solid #dbe4ef;border-radius:10px}}.node,.weight{{text-anchor:middle;font-weight:bold;fill:#172033}}.weight{{paint-order:stroke;stroke:white;stroke-width:5px}}.answer{{border-left:5px solid #22c55e;padding:10px 14px;background:#f0fdf4}}</style></head><body>
<h1>CS 505 Adjacency Matrix — Python Results</h1><p>Green matrix cells are connections (1). Gray cells are no connection (0).</p>
<section class='card'><h2>1. Relation adjacency matrices</h2>{matrix_html('R1: rows A1, columns A2',r1,a1,a2)}{relation_svg(a1,a2,r1,'R1 visual: y − x = 2')}{matrix_html('R2: rows A2, columns A3',r2,a2,a3)}{relation_svg(a2,a3,r2,'R2 visual: y − x = 1')}<p class='answer'>R2 is all zeros because no value in A3 is one greater than a value in A2.</p></section>
<section class='card'><h2>2. Shortest path with an adjacency matrix</h2><p>Example answer: <b>{' → '.join(data['path_labels'])}</b>, total weight <b>{data['distance']}</b>. Red marks the winning path.</p>{graph_svg(data['weighted_graph'],data['graph_labels'],data['path'])}<pre>SET every distance to infinity
SET the starting distance to 0
WHILE an unvisited vertex remains
    SET current to the unvisited vertex with smallest distance
    FOR each possible neighbor in current's matrix row
        IF an edge exists AND the new distance is smaller
            SET the neighbor's distance to the new distance
            SET its previous vertex to current
        END IF
    END FOR
    MARK current visited
END WHILE
FOLLOW previous vertices backward to build the path</pre></section>
<section class='card'><h2>3. Time and space complexity</h2><table><tr><th>Operation</th><th>Time</th><th>Total graph space</th><th>Simple reason</th></tr>{comp_rows}</table><p class='answer'>Main idea: the matrix always stores V × V cells, so graph storage is O(V²), even if only a few edges exist.</p></section>
<section class='card'><h2>4. Can A and B be added?</h2>{matrix_html('A',a)}{matrix_html('B',b)}<p class='answer'>{data['add_message']} Addition needs the exact same dimensions.</p></section>
<section class='card'><h2>5–6. Can A and B be multiplied?</h2><p class='answer'>{data['multiply_message']}</p>{matrix_html('A × B',data['product'])}<p>First result example: (1×7) + (2×9) + (3×11) = 58.</p></section>
<section class='card'><h2>7. Solve the system</h2><pre>3x + 2y − z = 1
2x − y + 3z = −3
x + y + z = 2</pre><p class='answer'>x = {solution[0]:g}, y = {solution[1]:g}, z = {solution[2]:g}</p><p>Gauss-Jordan elimination changes the augmented matrix until the left side becomes the identity matrix. The final right column is the solution.</p></section>
<section class='card'><h2>8. How matrices represent graphs</h2><p>{data['graph_explanation']}</p></section>
<section class='card'><h2>9. Matrix operations in computer science</h2><p>{data['cs_uses']}</p></section>
<section class='card'><h2>10. Determinant</h2>{matrix_html('A',data['special_a'])}<p><code>det(A) = 2(4×3 − 6×8) − 3(1×3 − 6×6) + 1(1×8 − 4×6)</code></p><p class='answer'>det(A) = {data['determinant']:g}</p></section>
<section class='card'><h2>11. Inverse</h2>{matrix_html('A⁻¹',data['inverse'])}<p>The code joins A to the identity matrix and uses row operations until A becomes the identity. The other half then becomes A⁻¹.</p></section>
<section class='card'><h2>12. Eigenvalues and eigenvectors</h2>{matrix_html('A =',data['eigen_a'])}<p class='answer'>Eigenvalue λ₁ = {eigvals[0]:g}, eigenvector ≈ {eigvecs[0]}<br>Eigenvalue λ₂ = {eigvals[1]:g}, eigenvector ≈ {eigvecs[1]}</p><p>Equivalent scaled vectors are (1, 1) for λ=4 and (1, −1) for λ=2. Eigenvectors may point in the opposite direction and still be correct.</p></section>
</body></html>"""
    out=OUTPUT_DIR/"adjacency_matrix_report.html"
    out.write_text(report,encoding="utf-8")
    return out


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    relations=problem_1_relation_matrices()
    weighted_graph=[[0,4,2,0,0],[4,0,1,5,0],[2,1,0,8,10],[0,5,8,0,2],[0,0,10,2,0]]
    graph_labels=["A","B","C","D","E"]
    distance,path=problem_2_shortest_path(weighted_graph,0,4)
    a=[[1,2,3],[4,5,6]]; b=[[7,8],[9,10],[11,12]]
    can_add,_,add_message=problem_4_can_add(a,b)
    _,multiply_message=problem_5_can_multiply(a,b)
    product=problem_6_multiply(a,b)
    solution,steps=problem_7_solve_linear_system([[3,2,-1],[2,-1,3],[1,1,1]],[1,-3,2])
    special_a=[[2,3,1],[1,4,6],[6,8,3]]
    determinant=problem_10_determinant(special_a)
    inverse=problem_11_inverse(special_a)
    eigen_a=[[3,1],[1,3]]
    eigen=problem_12_eigen_2x2(eigen_a)
    save_csv("problem_6_product.csv",product)
    save_csv("problem_7_solution.csv",[["x",solution[0]],["y",solution[1]],["z",solution[2]]])
    save_csv("problem_11_inverse.csv",inverse)
    data=dict(relations=relations,weighted_graph=weighted_graph,graph_labels=graph_labels,distance=distance,path=path,path_labels=[graph_labels[i] for i in path],complexities=problem_3_complexity_table(),a=a,b=b,can_add=can_add,add_message=add_message,multiply_message=multiply_message,product=product,solution=solution,steps=steps,graph_explanation=problem_8_graph_explanation(),cs_uses=problem_9_computer_science_uses(),special_a=special_a,determinant=determinant,inverse=inverse,eigen_a=eigen_a,eigen=eigen)
    report=create_report(data)
    # Optional packages add PNG heatmaps and graphs. The HTML report and all
    # calculations still work if the packages have not been installed.
    from package_visuals import create_matrix_package_visuals
    create_matrix_package_visuals(data, OUTPUT_DIR)
    print("CS 505 Adjacency Matrix Solver\n")
    print("R1 matrix:\n"+format_matrix(relations[3]))
    print("\nR2 matrix:\n"+format_matrix(relations[4]))
    print(f"\nShortest path: {' -> '.join(data['path_labels'])}; weight = {distance}")
    print(f"\nMatrix addition: {add_message}")
    print(f"Matrix multiplication: {multiply_message}\nA x B:\n{format_matrix(product)}")
    print(f"\nLinear system: x={solution[0]:g}, y={solution[1]:g}, z={solution[2]:g}")
    print(f"\nDeterminant: {determinant:g}\nInverse:\n{format_matrix(inverse,5)}")
    print(f"\nEigenvalues/eigenvectors: {eigen}")
    print(f"\nVisual report:\n{report}")


if __name__ == "__main__":
    main()
