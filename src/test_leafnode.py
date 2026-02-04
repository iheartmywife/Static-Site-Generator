import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_eq(self):
            node1 = LeafNode("p", "baby's first p tags", {"mi attribute": "es su attribute"})
            node2 = LeafNode("p", "baby's first p tags", {"mi attribute": "es su attribute"})
            self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = LeafNode("Title", "baby's first T tags", {"mi attribute": "es su attribute"})
        node2 = LeafNode("p", "baby's first p tags", {"su attribute": "es mi attribute"})
        self.assertNotEqual(node1, node2)