import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if isinstance(node, TextNode):
                if node.text_type != TextType.TEXT:
                    new_nodes.append(node)
                    continue
                text = node.text
                original_is_textnode = True
            else:
                text = node
                original_is_textnode = False

            delimiter_count = text.count(delimiter)

            if delimiter_count % 2 == 1:
                raise Exception(f"Invalid markdown syntax. Delimiter {delimiter} must wrap the desired text")

            if delimiter_count == 0:
                if original_is_textnode:
                    new_nodes.append(node)
                else:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                continue

            raw_text = text.split(delimiter)
            for index in range(0, len(raw_text)):
                if index % 2 == 0 or index == 0:
                    new_nodes.append(TextNode(raw_text[index], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(raw_text[index], text_type))
        return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
