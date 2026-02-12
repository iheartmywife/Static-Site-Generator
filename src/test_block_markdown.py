import unittest

from block_markdown import markdown_to_blocks, Blocktype, block_to_block_type, markdown_to_html_node

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

        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

        def test_headers(self):
            md = """
# This is h1

## This is h2

### This is h3

#### This is h4

##### This is h5

###### This is h6
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><h1>This is h1</h1><h2>This is h2</h2><h3>This is h3</h3><h4>This is h4</h4><h5>This is h5</h5><h6>This is h6</h6></div>"
            )

        def test_quotes(self):
            md = """
> This is a quote block with a space after >
> Which can be **tricky** sometimes  
> to parse through

>This is a quote block without a space after >
>Which can be tricky in its own right
>And create some troubles

> This is a quote block that alternates
>Between a space after the > and
> No space after the >
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><blockquote>This is a quote block with a space after > Which can be <b>tricky</b> sometimes to parse through</blockquote><blockquote>This is a quote block without a space after > Which can be tricky in its own right And create some troubles</blockquote><blockquote>This is a quote block that alternates Between a space after the > and No space after the ></blockquote></div>",
            )

        def test_unordered_lists(self):
            md = """
- This is an unordered list block
- Which can be **tricky** sometimes  
- to parse through

- This is another unordered list block
- with several
- unnecessary
- newlines
- and thus
- way more
- li elements
- than is necessary

- This is one more unordered list block
- only two lines this time
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html, "<div><ul><li>This is an unordered list block</li><li>Which can be <b>tricky</b> sometimes</li><li>to parse through</li></ul><ul><li>This is another unordered list block</li><li>with several</li><li>unnecessary</li><li>newlines</li><li>and thus</li><li>way more</li><li>li elements</li><li>than is necessary</li></ul><ul><li>This is one more unordered list block</li><li>only two lines this time</li></ul></div>"
            )

        def test_ordered_lists(self):
            md = """
1. This is an ordered list block
2. Which can be **tricky** sometimes  
3. to parse through

1. This is another ordered list block
2. with several
3. unnecessary
4. newlines
5. and thus
6. way more
7. li elements
8. than is necessary
9. This is another ordered list block
10. with several
11. unnecessary
12. newlines
13. and thus
14. way more
15. li elements
16. than is necessary

1. This is one more ordered list block
2. only two lines this time
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html, "<div><ol><li>This is an ordered list block</li><li>Which can be <b>tricky</b> sometimes</li><li>to parse through</li></ol><ol><li>This is another ordered list block</li><li>with several</li><li>unnecessary</li><li>newlines</li><li>and thus</li><li>way more</li><li>li elements</li><li>than is necessary</li><li>This is another ordered list block</li><li>with several</li><li>unnecessary</li><li>newlines</li><li>and thus</li><li>way more</li><li>li elements</li><li>than is necessary</li></ol><ol><li>This is one more ordered list block</li><li>only two lines this time</li></ol></div>"
            )

        def test_paragraph_with_all_inline_styles(self):
            md = """
This has **bold**, _italic_, `code`, a [link](https://example.com), and an ![image](https://example.com/img.png).
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                '<div><p>This has <b>bold</b>, <i>italic</i>, <code>code</code>, a <a href="https://example.com">link</a>, and an <img src="https://example.com/img.png" alt="image"></img>.</p></div>',
            )

        def test_all_block_types(self):
            md = """
# Heading one

This is a paragraph with **bold** and _italic_.

```
code block line 1
code block line 2
```


> This is a quote with `code`.

- unordered one
- unordered two

1. ordered one
2. ordered two
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div>"
                "<h1>Heading one</h1>"
                "<p>This is a paragraph with <b>bold</b> and <i>italic</i>.</p>"
                "<pre><code>code block line 1\ncode block line 2\n</code></pre>"
                "<blockquote>This is a quote with <code>code</code>.</blockquote>"
                "<ul><li>unordered one</li><li>unordered two</li></ul>"
                "<ol><li>ordered one</li><li>ordered two</li></ol>"
                "</div>",
            )