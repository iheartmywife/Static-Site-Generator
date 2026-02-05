import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node in code mode with a load of code...brode", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node in code mode with a load of code...brode")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.url/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://img.url/cat.png", "alt": "alt text"},
        )

    def test_markdown_to_textnodes_bold(self):
        old_nodes = [
            "This is text with only plain text",
            "This is text with a **bolded phrase** in the middle",
            "This is text with only plain text",
        ]
        desired_outcome = [
            TextNode("This is text with only plain text", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("This is text with only plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, desired_outcome)

    def test_markdown_to_textnodes_italic(self):
        old_nodes = [
            "This is text with only plain text",
            "This is text with an _italic phrase_ in the middle",
            "This is text with only plain text",
        ]
        desired_outcome = [
            TextNode("This is text with only plain text", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("This is text with only plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, desired_outcome)

    def test_markdown_to_textnodes_code(self):
        old_nodes = [
            "This is text with only plain text",
            "This is text with a 'code phrase' in the middle",
            "This is text with only plain text",
        ]
        desired_outcome = [
            TextNode("This is text with only plain text", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code phrase", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("This is text with only plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "'", TextType.CODE)
        self.assertEqual(new_nodes, desired_outcome)

    def test_non_text_textnode(self):
        old_nodes = [
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode("code phrase", TextType.CODE),
            TextNode("This is a text with a **bolded phrase** in the middle", TextType.TEXT),
        ]
        desired_outcome = [
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode("code phrase", TextType.CODE),
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, desired_outcome)

        """
        TextType(Enum):
        TEXT = "text" IMPLEMENTED
        BOLD = "bold" IMPLEMENTED
        ITALIC = "italic" IMPLEMENTED
        CODE = "code" IMPLEMENTED
        LINK = "link" IMPLEMENTED
        IMAGE = "image" 
        """

        """
            def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        """

if __name__ == "__main__":
    unittest.main()