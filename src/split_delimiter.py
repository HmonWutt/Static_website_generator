from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for each in old_nodes:
        if each.text_type == TextType.TEXT:
            new_nodes.extend(helper(each,delimiter,text_type))
    return new_nodes


def helper(node,delimiter,type):
    new_nodes = []
    delimiter_count = 0
    temp = ""
    for char in node.text:
        if char == delimiter:
            if delimiter_count==1 and temp:
                node = TextNode(temp,type)
                temp = ""
                delimiter_count=0
                new_nodes.append(node)
            elif delimiter_count == 0 and temp:
                node = TextNode(temp,TextType.TEXT)
                temp = ""
                delimiter_count+=1
                new_nodes.append(node)

        else:
            temp+=char
    if delimiter_count == 1:
        raise Exception("delimiter unmatched")
    if temp:
        node = TextNode(temp, TextType.TEXT)
        new_nodes.append(node)
    return new_nodes

    



