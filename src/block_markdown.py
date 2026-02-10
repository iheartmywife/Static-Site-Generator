from enum import Enum

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
                if line.startswith((">", "> ")):
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
