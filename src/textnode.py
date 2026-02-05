from enum import Enum
from htmlnode import LeafNode, HTMLNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

# Added this, saw I didnt need it, didnt want to delete it on the off chance I need again
""" 
class Delimiters(Enum):
    BOLD = '**'
    ITALIC = '_'
    CODE = "'"

    def match_delimiter(delimiter):
        match delimiter:
            case Delimiters.BOLD:
                return TextType.BOLD
            case Delimiters.ITALIC:
                return TextType.ITALIC
            case Delimiters.CODE:
                return TextType.CODE
        raise Exception("Delimiter not found. Please use ** for bold, _ for italic, or ' for code")
"""

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    
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

