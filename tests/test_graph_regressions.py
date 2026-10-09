"""Focused regressions for the runnable CS-505/CS-508 examples."""

import importlib.util
from pathlib import Path

import math
import unittest


ROOT = Path(__file__).parents[1]


def load(relative):
    spec = importlib.util.spec_from_file_location(relative.stem, relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GraphRegressionTests(unittest.TestCase):
    def test_ford_fulkerson_rejects_identical_source_and_sink(self):
        module = load(ROOT / "CS-505/Module-Five-Graph-Theory/graph_algorithms.py")
        with self.assertRaisesRegex(ValueError, "different"):
            module.ford_fulkerson({"s": {"t": 1}, "t": {}}, "s", "s")
        self.assertEqual(module.ford_fulkerson({"s": {"t": 2}, "t": {}}, "s", "t")[0], 2)


    def test_symmetric_eigenvectors_are_finite_normalized_and_valid(self):
        module = load(ROOT / "CS-505/Module-Seven-Adjacency-Matrices/adjacency_matrix_pycharm.py")
        for matrix in ([[1, 0], [0, 1]], [[2, 0], [0, 3]], [[4, 0], [0, 4]]):
            values, vectors = module.problem_12_eigen_2x2(matrix)
            for value, vector in zip(values, vectors):
                self.assertTrue(all(math.isfinite(v) for v in vector))
                self.assertAlmostEqual(sum(v * v for v in vector), 1, places=5)
                self.assertAlmostEqual(matrix[0][0] * vector[0] + matrix[0][1] * vector[1], value * vector[0], places=5)
                self.assertAlmostEqual(matrix[1][0] * vector[0] + matrix[1][1] * vector[1], value * vector[1], places=5)


    def test_empty_graph_has_documented_no_path_result(self):
        module = load(ROOT / "CS-508/Module-Eight-Graph-Traversal/cs508_graph_model.py")
        self.assertEqual(module.path_extremes({"vertices": [1], "edges": [], "directed": False}), (None, None))


    def test_trie_normalizes_lookup_like_insert(self):
        module = load(ROOT / "CS-508/Module-Seven-Trie/trie_diagram.py")
        trie = module.Trie()
        trie.insert("  LaRk ")
        self.assertTrue(trie.contains(" lark "))
