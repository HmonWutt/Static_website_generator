import re
import os
import shutil
from pathlib import Path
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
        tag,type,text = block_to_tag_and_text(block)
        if tag != "p":
            children = [LeafNode(tag, text)]
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
            return "p", type, re.findall(BlockType.PARAGRAPH.value,block)[0]
        case "HEADING":
            return "h3",type,re.findall(BlockType.HEADING.value,block)[0]
        case "QUOTE":
            return "span",type,re.findall(BlockType.QUOTE.value,block)[0]
        case "CODE":
            return "pre",type,re.findall(BlockType.CODE.value,block)[0]
        case "UNORDERED_LIST":
            return "ul",type,re.findall(BlockType.UNORDERED_LIST.value,block)[0]
        case "ORDERED_LIST":
            return "ol",type,re.findall(BlockType.ORDERED_LIST.value,block)[0]

def extract_title(markdown):
    pattern =  r"^# (.*)"
    lines = markdown.split("\n\n")
    for line in lines:
        stripped = line.strip("\n")
        if stripped:
            if re.search(pattern,stripped):
                return re.search(pattern,stripped).group(1)
            Exception("No title found")

def copy_files(src_dir):
    if not os.path.exists(src_dir):
        raise Exception("source path not valid")
    if os.path.isfile(src_dir):
        return src_dir
    return helper_copy_files(src_dir,[])

def helper_copy_files(path,file_paths):
    if os.path.isfile(path):
        file_paths.append(path)
        print("src: ",path)
        return file_paths
    sub_dirs = os.listdir(path) 
    for sub_dir in sub_dirs:
        joined_path = os.path.join(path,sub_dir)
        helper_copy_files(joined_path, file_paths)
    return file_paths

def paste_files(filepaths, destination_dir):
    for filepath in filepaths:
        src_path = os.path.join(*filepath.split(os.sep)[:])
        dest_path = os.path.join(destination_dir,src_path)
        dir = os.path.dirname(dest_path)
        os.makedirs(dir,exist_ok=True)
        shutil.copy(filepath,dest_path)
        print("dest: ",dest_path)

def empty_dir(dir):
    dir = Path(dir)
    for item in dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = ""
    template_content = ""
    with open(from_path, 'r') as markdown:
        markdown_content = markdown.read()
    
    with open(template_path,'r')as template:
        template_content = template.read()
    title = extract_title(markdown_content)
    markdown_to_html = markdown_to_html_node(markdown_content).to_html()
    content = template_content.format(title=title, content=markdown_to_html )
    with open(dest_path,'x') as output:
        output.write(content)



