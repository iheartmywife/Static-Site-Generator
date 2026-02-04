import unittest
from htmlnode import ParentNode
from htmlnode import LeafNode

class test_parentnode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child", {"href": "https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span href=\"https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f\">child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"href": "https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b href=\"https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f\">grandchild</b></span></div>",
        )

    def test_to_html_with_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild", {"href": "https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_children(self):
        grandchild_node = LeafNode("b", "grandchild", {"href": "https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()