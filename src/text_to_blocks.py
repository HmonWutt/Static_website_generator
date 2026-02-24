import re
from enum import Enum
from split_delimiter import text_to_textnodes
from textnode import text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
class BlockType(Enum):
    PARAGRAPH=r"^(?![#+ |> ?|```|\-|\d.])([\s\S]*)"
    HEADING = r"^#+ ([\s\S]*)"
    QUOTE = r"^> ?([\s\S]*)"
    CODE = r"^```\n([\s\S]*)```$"
    UNORDERED_LIST = r"^\- ([\s\S]*)"
    ORDERED_LIST = r"^\d. ([\s\S]*)"

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



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) 
    children = []
    html = []
    for block in blocks:
        tag,text = block_to_tag_and_text(block)
        if tag == "pre":
            children = [LeafNode("code", text)]
        else:
            replace_newline = re.sub("\n"," ",text)
            children_textnodes = text_to_textnodes(replace_newline)
            for each in children_textnodes:
                children.append(text_node_to_html_node(each))
        node = ParentNode(tag,children)
        html.append(node)
        children=[]
     
    return ParentNode("div",html)

        
def block_to_tag_and_text(block):
    type = block_to_block_type(block)
    match type:
        case "PARAGRAPH":
            return "p", re.findall(BlockType.PARAGRAPH.value,block)[0]
        case "HEADING":
            return "h3",re.findall(BlockType.HEADING.value,block)[0]
        case "QUOTE":
            return "p",re.findall(BlockType.QUOTE.value,block)[0]
        case "CODE":
            return "pre",re.findall(BlockType.CODE.value,block)[0]
        case "UNORDERED_LIST":
            return "ul",re.findall(BlockType.UNORDERED_LIST.value,block)[0]
        case "ORDERED_LIST":
            return "ol",re.findall(BlockType.ORDERED_LIST.value,block)[0]

def extract_title(markdown):
    pattern =  r"^# (.*)"
    lines = markdown.split("\n\n")
    for line in lines:
        stripped = line.strip("\n")
        if stripped:
            if re.search(pattern,stripped):
                return re.search(pattern,stripped).group(1)
            raise Exception("No title found")
