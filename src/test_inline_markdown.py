import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TextInlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_images_one(self):
        pre_regex_text = f'![this is test alt text for our function](image link)'
        post_regex_text = [("this is test alt text for our function", "image link")]

        self.assertEqual(
            extract_markdown_images(pre_regex_text), 
            post_regex_text)

    def test_extract_markdown_images_two(self):
        
        pre_regex_text_two = f'[this is test alt text for our function](image link)'
        post_regex_text_two = []

        self.assertEqual(
            extract_markdown_images(pre_regex_text_two), 
            post_regex_text_two)
        
    def test_extract_markdown_images_three(self): #feeding multiple links
        pre_regex_text = f'![this is test alt text for our function](image link). ![this is test alt text for our function](image link). ![this is test alt text for our function](image link)'
        post_regex_text = [("this is test alt text for our function", "image link"), ("this is test alt text for our function", "image link"), ("this is test alt text for our function", "image link")]

        self.assertEqual(
            extract_markdown_images(pre_regex_text), 
            post_regex_text)

    def test_extract_markdown_links_one(self):
        pre_regex_text = f'[this is test alt text for our function](link)'
        post_regex_text = [("this is test alt text for our function", "link")]
        self.assertEqual(post_regex_text, extract_markdown_links(pre_regex_text))


    def test_extract_markdown_links_two(self):
        pre_regex_text_two = f'![this is test alt text for our function](link)'
        post_regex_text_two = []
        self.assertEqual(post_regex_text_two, extract_markdown_links(pre_regex_text_two))

    def test_extract_markdown_links_three(self): #feeding multiple links
        pre_regex_text = f'[this is test alt text for our function](link). [this is test alt text for our function](link). [this is test alt text for our function](link)'
        post_regex_text = [("this is test alt text for our function", "link"), ("this is test alt text for our function", "link"), ("this is test alt text for our function", "link")]
        self.assertEqual(
            extract_markdown_links(pre_regex_text), 
            post_regex_text)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_lead_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with no lead text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with no lead text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_no_markdown(self):
        node = TextNode("Simple node with no special markdown", TextType.TEXT)
        self.assertEqual([node], split_nodes_image([node]))

    def test_non_text_textnodes_images(self):
        nodes = [
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("bold", TextType.BOLD),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                 ]
        self.assertEqual(nodes, split_nodes_image(nodes))

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_lead_text(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png) with no leading text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with no leading text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_no_markdown(self):
        node = TextNode("Simple node with no special markdown", TextType.TEXT)
        self.assertEqual([node], split_nodes_link([node]))

    def test_non_text_textnodes_links(self):
        nodes = [
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("bold", TextType.BOLD),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                 ]
        self.assertEqual(nodes, split_nodes_link(nodes))