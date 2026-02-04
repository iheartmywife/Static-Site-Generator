import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "baby's first p tags", ["a", "href", "h1"],)
        node2 = HTMLNode("p", "baby's first p tags", ["a", "href", "h1"],)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("Title", "baby's first T tags", ["p", "a", "href", "h1"], {})
        node2 = HTMLNode("p", "baby's first p tags", ["a", "href", "h1"], {})
        self.assertNotEqual(node1, node2)

    def test_props_to_html(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node1 = HTMLNode("Title", "baby's first T tags", ["p", "a", "href", "h1"], test_props)
        return node1.props_to_html == ' href="https://www.google.com" target="_blank"'
