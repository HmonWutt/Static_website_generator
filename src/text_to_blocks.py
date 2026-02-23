import re
from enum import Enum
class BlockType(Enum):
    PARAGRAPH=r"^(?![#+ |> ?|```|\-|\d.])"
    HEADING = r"^#+ "
    QUOTE = r"^> ?"
    CODE = r"^```"
    UNORDERED_LIST = r"^\- "
    ORDERED_LIST = r"^\d. "

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks  = []
    length = len(blocks)
    for i in range(length):
        if blocks[i]:
            new_blocks.append(blocks[i].strip("\n"))
    return new_blocks

def block_to_block_type(block):
    for type in BlockType:
        if re.search(type.value,block):
            return type.name




