# Programs Added From the CS 505/CS 508 Work Sessions

This index lists the programs, notebooks, and generated examples added from the
coursework work sessions. Each assignment is kept in its matching course and
module directory.

## CS 505

- `CS-505/Module-Five-Graph-Theory/` — Prim, Kruskal, Ford-Fulkerson, testing,
  complexity analysis, and Jupyter notebook.
- `CS-505/Module-Five-Combinatorics/` — permutations, combinations, stars and
  bars, Python walkthrough, and Jupyter notebook.
- `CS-505/Module-Six-Trees/` — Module Six tree activity document builder.
- `CS-505/Module-Seven-Boolean-Algebra/` — Boolean simplification, NAND-only
  implementation, truth tables, circuit diagrams, CSV output, and HTML report.
- `CS-505/Module-Seven-Adjacency-Matrices/` — relations, Dijkstra, matrix
  operations, linear systems, determinant, inverse, eigenvalues, CSV output,
  and HTML report.
- `CS-505/Module-Seven-Activity-Builders/` — Word-template builder for the two
  Module Seven activities.
- `CS-505/Discrete-Modeling-Paper/` — document-generation script for the
  discrete-modeling paper.

## CS 508

- `CS-508/Project-One-Attendee-Manager/` — Java conference attendee manager and
  deliverable builder.
- `CS-508/Module-Seven-BST-Validity-Checker/` — Java BST validity checker.
- `CS-508/Module-Seven-Trie/` — Python trie model, high-resolution SVG output,
  node CSV, text tree, and journal builder.

## Supporting builders

`Supporting-Document-Builders/` contains scripts that populated templates,
added pseudocode explanations, and generated notebooks. For document builders,
place the required source template in the script folder's `input/` directory;
the script writes its result to `output/`.

## Running the Python projects

Projects with third-party dependencies include a `requirements.txt` file. From
that project directory, run:

```bash
python3 -m pip install -r requirements.txt
python3 <program_name>.py
```

The main Boolean algebra, adjacency-matrix, and trie programs include fallback
behavior when optional visualization packages are not installed.
