import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("This is text node 1", TextType.ITALIC)
        node2 = TextNode("This is text node 2", TextType.IMAGE)
        self.assertNotEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("This is text node 1", TextType.ITALIC, "https://www.markdownguide.org/cheat-sheet/")
        node2 = TextNode("This is text node 2", TextType.IMAGE)
        self.assertIsNotNone(node1.url)
        self.assertIsNone(node2.url)

if __name__ == "__main__":
    unittest.main()