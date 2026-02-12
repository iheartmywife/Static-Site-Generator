from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import LeafNode, ParentNode, HTMLNode

def markdown_to_blocks(markdown):
    filtered_blocks = []
    blocks = str.split(markdown, "\n\n")
    for block in blocks:
        block = str.strip(block)
        if block.isspace() or len(block) == 0:
            continue
        else:
            filtered_blocks.append(block)
    return filtered_blocks

class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def determine_blocktype_specific_tag(blocktype, text):
    match blocktype:
        case Blocktype.HEADING:
            if text.startswith("# "):
                return "h1"
            if text.startswith("## "):
                return "h2"
            if text.startswith("### "):
                return "h3"
            if text.startswith("#### "):
                return "h4"
            if text.startswith("##### "):
                return "h5"
            if text.startswith("###### "):
                return "h6"


def block_to_block_type(markdown):
    unformatted_starting_text = str.split(markdown, "\n")
    formatted_starting_text = []
    for text in unformatted_starting_text:
        if text.isspace() or len(text) == 0:
            continue
        else:
            formatted_starting_text.append(text)
    starting_text = formatted_starting_text[0]
    if starting_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return Blocktype.HEADING
    if starting_text.startswith("```") and formatted_starting_text[-1].endswith("```"):
        return Blocktype.CODE
    if starting_text.startswith((">", "> ")) and every_line_valid(Blocktype.QUOTE, formatted_starting_text):
        return Blocktype.QUOTE
    if starting_text.startswith("- ") and every_line_valid(Blocktype.UNORDERED_LIST, formatted_starting_text):
        return Blocktype.UNORDERED_LIST
    if every_line_valid(Blocktype.ORDERED_LIST, formatted_starting_text):
        return Blocktype.ORDERED_LIST
    return Blocktype.PARAGRAPH

def every_line_valid(block_type, lines):
    match block_type:
        case Blocktype.QUOTE:
            for line in lines:
                if line.startswith((">")):
                    continue
                else:
                    return False
            return True
        case Blocktype.UNORDERED_LIST:
            for line in lines:
                if line.startswith("- "):
                    continue
                else:
                    return False
            return True
        case Blocktype.ORDERED_LIST:
            i = 1
            for line in lines:
                if line.startswith(f"{i}. "):
                    i += 1
                    continue
                else:
                    return False
            return True
    raise Exception("Please enter a valid blocktype: quote, unordered list, or ordered list")

def markdown_to_html_node(markdown):
        html_nodes = []
        blocks = markdown_to_blocks(markdown)
        for block in blocks:
            block_type = block_to_block_type(block)
            block_tag = determine_tag(block_type, block)
            if block_type == Blocktype.CODE:
                raw_text = block.split("\n")
                inner = "\n".join(raw_text[1:-1])
                no_fences = inner + "\n"
                code_node = LeafNode("code", no_fences)
                parent_node = ParentNode("pre", [code_node])
                html_nodes.append(parent_node)
            else:
                content = block_to_content(block_type, block)
                block_children = determine_children(content, block_type=block_type)
                node = ParentNode(block_tag, block_children)
                html_nodes.append(node)
        final_node = ParentNode("div", children=html_nodes)
        return final_node

def block_to_content(block_type, text):
    match block_type:
        case Blocktype.PARAGRAPH:
            content_lines = text.split("\n")
            content = " ".join(content_lines)
            return content
        case Blocktype.HEADING:
            content_lines = text.split()
            content = " ".join(content_lines[1:])
            return content
        case Blocktype.QUOTE:
            raw_lines = text.split("\n")
            content_lines = []
            for line in raw_lines:
                if line.startswith("> "):
                    content_lines.append(line[2:].strip())
                else:
                    content_lines.append(line[1:].strip())
            content = " ".join(content_lines)
            return content
        case Blocktype.UNORDERED_LIST:
            raw_lines = text.split("\n")
            content = []
            for line in raw_lines:
                content.append(line[2:].strip())
            return content
        case Blocktype.ORDERED_LIST:
            raw_lines = text.split("\n")
            content = []
            i = 1
            for line in raw_lines:
                if i <= 9:
                    content.append(line[3:].strip())
                    i += 1
                    continue
                if 9 < i < 100:
                    content.append(line[4:].strip())
                    i += 1
                    continue
                if 99 < i < 1000:
                    content.append(line[4:].strip())
                    continue
            return content
        #code not included because it requires special handling inside markdown_to_html_node

def determine_tag(block_type, text):
    match block_type:
        case Blocktype.PARAGRAPH:
            return "p"
        case Blocktype.HEADING:
            return determine_blocktype_specific_tag(Blocktype.HEADING, text)
        case Blocktype.QUOTE:
            return "blockquote"
        case Blocktype.UNORDERED_LIST:
            return "ul"
        case Blocktype.ORDERED_LIST:
            return "ol"
        #code not included because it requires special handling inside markdown_to_html_node

def determine_children(block_text, block_type=None):
    html_nodes = []
    if block_type == Blocktype.UNORDERED_LIST or block_type == Blocktype.ORDERED_LIST:
        for line in block_text:
            line_children = determine_children(line)
            list_node = ParentNode("li", line_children)
            html_nodes.append(list_node)
            
    else:
        text_nodes = text_to_textnodes(block_text)
        for tn in text_nodes:
            html_n = text_node_to_html_node(tn)
            html_nodes.append(html_n)
    return html_nodes
