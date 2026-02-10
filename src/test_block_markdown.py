import unittest

from block_markdown import markdown_to_blocks, Blocktype, block_to_block_type, every_line_valid

class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_excessive_whitespace(self):
            md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_leading_trailing_newlines(self):
            md = """



This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_single_block(self):
            md = "This is **bolded** paragraph"
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph"
                ],
            )

        def test_markdown_to_blocks_whitespace_only(self):
            md = "                    "
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [],
            )

        def test_block_to_block_type_heading(self):
            block_text = "# this is a heading"
            result = Blocktype.HEADING
            self.assertEqual(block_to_block_type(block_text), result)

        def test_block_to_block_type_code(self):
            block_text = """
```
this is a multi-line
code block.```
"""
            result = Blocktype.CODE
            self.assertEqual(block_to_block_type(block_text), result)

        def test_block_to_block_type_quote(self):
            block_text = """
>This is
>properly formatted
>quote text
>for markdown.
"""
            result = Blocktype.QUOTE
            self.assertEqual(block_to_block_type(block_text), result)

        def test_block_to_block_type_unordered_list(self):
            block_text = """
- This is
- properly formatted
- unordered_list text
- for markdown.
"""
            result = Blocktype.UNORDERED_LIST
            self.assertEqual(block_to_block_type(block_text), result)

        def test_block_to_block_type_ordered_list(self):
            block_text = """
1. This is
2. properly formatted
3. ordered_list text
4. for markdown.
"""
            result = Blocktype.ORDERED_LIST
            self.assertEqual(block_to_block_type(block_text), result)