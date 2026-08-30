import json
from pathlib import Path

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Prim, Kruskal, and Ford-Fulkerson\n",
                "Run the implementation cell, then run each example cell. No third-party packages are required."
            ],
        },
        {
            "cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": [
                "from graph_algorithms import (\n",
                "    ford_fulkerson, kruskal_msf, prim_mst, undirected_graph\n",
                ")\n",
            ],
        },
        {
            "cell_type": "markdown", "metadata": {},
            "source": ["## Minimum spanning tree examples\n", "Prim grows one tree; Kruskal joins components without cycles."],
        },
        {
            "cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": [
                "weighted_edges = [(\"A\", \"B\", 1), (\"A\", \"C\", 4), (\"B\", \"C\", 2),\n",
                "                  (\"B\", \"D\", 5), (\"C\", \"D\", 1), (\"D\", \"E\", 3)]\n",
                "vertices = {v for edge in weighted_edges for v in edge[:2]}\n",
                "print(prim_mst(undirected_graph(weighted_edges), \"A\"))\n",
                "print(kruskal_msf(vertices, weighted_edges))\n",
            ],
        },
        {
            "cell_type": "markdown", "metadata": {},
            "source": ["## Maximum-flow example\n", "The implementation uses BFS, so it is the Edmonds-Karp version of Ford-Fulkerson."],
        },
        {
            "cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": [
                "network = {\n",
                "    \"s\": {\"a\": 3, \"b\": 2},\n",
                "    \"a\": {\"b\": 1, \"t\": 2},\n",
                "    \"b\": {\"t\": 3},\n",
                "    \"t\": {},\n",
                "}\n",
                "ford_fulkerson(network, \"s\", \"t\")\n",
            ],
        },
    ],
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3"}},
    "nbformat": 4,
    "nbformat_minor": 5,
}
Path("outputs/graph_algorithms_notebook.ipynb").write_text(json.dumps(notebook, indent=2))
