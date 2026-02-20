from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for each in old_nodes:
        if each.text_type == TextType.TEXT:
            new_nodes.extend(helper(each,delimiter,text_type))
        else:
            new_nodes.append(each)
    return new_nodes


def helper(node,delimiter,type):
    if not node.text:
        return []
    new_nodes = []
    split_texts = node.text.split(delimiter)
    for ind, each in enumerate(split_texts):
        if each:
            if ind%2 ==0:
                new_nodes.append(TextNode(each,TextType.TEXT))
            else:
                new_nodes.append(TextNode(each,type))

    return new_nodes

    



