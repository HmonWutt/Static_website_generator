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
    PARAGRAPH=r"^(?!(?:#+ |> ?|```|\-|\d.))([\s\S]*)"
    HEADING = r"^(# ?[\s\S]*)"
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
    html = ""
    for block in blocks:
        html_node = block_to_tag_and_text(block)
        html+=html_node
    return html
        
def block_to_tag_and_text(block):
    type = block_to_block_type(block)
    match type:
        case "PARAGRAPH":
            text =  re.findall(BlockType.PARAGRAPH.value,block)[0]
            paragraph = md_paragraph_to_html(text)
            return paragraph
        case "HEADING":
            heading = re.findall(BlockType.HEADING.value,block)[0] 
            node = None
            heading_one_pattern = r"^#(?!#) ?([\s\S]*)"
            pattern = r"^#+ ?([\s\S]*)"
            if re.search(heading_one_pattern,heading):
                node = md_heading_to_html("h1",heading,pattern)
            else:
                node = md_heading_to_html("h2", heading,pattern)
            return node
        case "QUOTE":
            text = re.findall(BlockType.QUOTE.value,block)[0]
            quote = md_quote_to_html(text) 
            return quote
        case "CODE":
            text = re.findall(BlockType.CODE.value,block)[0]
            code = LeafNode("code",text)
            parent = ParentNode("pre",[code],None)
            return parent.to_html()
        case "UNORDERED_LIST":
            text = re.findall(BlockType.UNORDERED_LIST.value,block)[0]
            pattern = r'\n\-\s?'
            ul = md_list_to_html(text,pattern,"li","ul") 
            return ul
        case "ORDERED_LIST":
            pattern = '\n[0-9]. '
            text = re.findall(BlockType.ORDERED_LIST.value,block)[0]
            pattern = r'\n[0-9]+\.\s?'
            ol = md_list_to_html(text,pattern,"li","ol")
            return ol

def md_heading_to_html(tag, text,pattern):
    trimmed_text = re.findall(pattern,text)[0]
    node = LeafNode(tag,trimmed_text)
    return node.to_html()

def md_paragraph_to_html(text):
    no_newline = re.sub('\n'," ",text)
    text_nodes = text_to_textnodes(no_newline)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    node = ParentNode("p",html_nodes,None).to_html()
    return node

def md_list_to_html(text,pattern,child_tag,parent_tag):
    items = re.split(pattern,text)
    list_items_as_html = ""
    for item in items:
        text_nodes = text_to_textnodes(item)
        html_nodes = []
        for text_node in text_nodes:
            html_nodes.append(text_node_to_html_node(text_node))
            list_item = ParentNode(child_tag,html_nodes, None).to_html()
            list_items_as_html+=list_item
    return f"<{parent_tag}>{list_items_as_html}</{parent_tag}>"

def md_quote_to_html(text):
    lines = re.split(r"> ?",text)
    lines_joined = ""
    author = ""
    for line in lines:
        if line.startswith("--"):
            author = line
        else:
            lines_joined+=line
    quote_node = LeafNode("blockquote" ,lines_joined )
    if author:
        author_node = LeafNode("figcaption",author)
        node = ParentNode("figure", [quote_node,author_node],{"class": "quote"})
        return node.to_html()
    else:
        node = ParentNode("figure", [quote_node],{"class": "quote"})
        return node.to_html()



def extract_title(markdown):
    pattern =  r"^#(?!#) ?(.*)"
    lines = markdown.split("\n\n")
    stripped = lines[0].strip("\n")
    if stripped:
        if re.search(pattern,stripped):
            return re.search(pattern,stripped).group(1)
    raise Exception("No title found")

def copy_file_paths(src_dir):
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

def paste_files(src_filepaths, destination_dir):
    for src_filepath in src_filepaths:
        dest_path = create_dest_dir_path(src_filepath,destination_dir)
        shutil.copy(src_filepath,dest_path)
        print("dest: ",dest_path)

def create_dest_dir_path(source_filepath, dest_dir):
    src_path = os.path.join(*source_filepath.split(os.sep)[1:])
    dest_path = os.path.join(dest_dir,src_path)
    dir = os.path.dirname(dest_path)
    os.makedirs(dir,exist_ok=True)
    return dest_path

def create_dest_dir_path_dir_included(source_filepath, dest_dir):
    src_path = os.path.join(*source_filepath.split(os.sep)[1:])
    dest_path = os.path.join(dest_dir,src_path)
    dir = os.path.dirname(dest_path)
    path = os.path.join(dir, "index.html")
    os.makedirs(dir,exist_ok=True)
    return path

def write_file(filepath, content):
     with open(filepath,'x') as output:
        output.write(content)

def empty_dir(dir):
    dir = Path(dir)
    for item in dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def generate_pages_recursively(src_dir, template_path, dest_dir):
    print(f"Generating pages from {src_dir} to {dest_dir} using {template_path}")
    markdown_content = ""
    template_content = ""
    with open(template_path,'r')as template:
        template_content = template.read()
    content_filepaths = copy_file_paths(src_dir)
    for content_filepath in content_filepaths:
        with open(content_filepath, 'r') as markdown:
            markdown_content = markdown.read()
        title = extract_title(markdown_content)
        markdown_to_html = markdown_to_html_node(markdown_content)
        content = template_content.format(title=title, content=markdown_to_html )
        dest_path = create_dest_dir_path_dir_included(content_filepath,dest_dir)
        write_file(dest_path, content)
        


