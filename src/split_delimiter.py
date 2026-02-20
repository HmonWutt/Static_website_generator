import re
from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for each in old_nodes:
        if each.text_type == TextType.TEXT:
            new_nodes.extend(helper_split_nodes_delimiter(each,delimiter,text_type))
        else:
            new_nodes.append(each)
    return new_nodes


def helper_split_nodes_delimiter(node,delimiter,type):
    if not node.text:
        return []
    new_nodes = []
    split_texts = node.text.split(delimiter)
    if len(split_texts)%2==0:
        raise Exception("Missing closing delimiter, formatted wrong")
    for ind, each in enumerate(split_texts):
        if each:
            if ind%2 ==0:
                new_nodes.append(TextNode(each,TextType.TEXT))
            else:
                new_nodes.append(TextNode(each,type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern,text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern,text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for each in old_nodes:
        if each.text_type == TextType.TEXT:
            new_nodes.extend(helper_split_nodes(each.text,extract_markdown_images,"![",TextType.IMAGE))
        else:
            new_nodes.append(each)
    return new_nodes

def helper_split_nodes(text,callback, start,type):
    if not text:
        return []
    copy = text 
    new_nodes = []
    images = callback(text)
    while images:
        image= images.pop(0)
        delimiter = start+"](".join(image)+")"
        split_texts = copy.split(delimiter,1)
        text_before_image = split_texts[0]
        if text_before_image:
            new_nodes.append(TextNode(text_before_image, TextType.TEXT)) 
        new_nodes.append(TextNode(image[0],type,image[1]))
        copy = split_texts[1]
    if copy:
        new_nodes.append(TextNode(copy,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes=[]
    for each in old_nodes:
        if each.text_type == TextType.TEXT:
            new_nodes.extend(helper_split_nodes(each.text,extract_markdown_links,"[",TextType.LINK))
        else:
            new_nodes.append(each)
    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text,TextType.TEXT)]
    old_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
    old_nodes = split_nodes_delimiter(old_nodes,"_",TextType.ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes,"`",TextType.CODE)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    return old_nodes


