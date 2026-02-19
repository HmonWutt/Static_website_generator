from htmlnode import HTMLNode
from leafnode import LeafNode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent element must have a tag")
        if not self.children:
            raise ValueError("parent element must have children")
        return self.getChildren(self, "")

    def getChildren(self,node, result):
        if type(node) == LeafNode:
            if not node.tag :
                return node.value
            return node.to_html()
        tmp = ""
        for each in node.children:
            tmp += self.getChildren(each,result)
        return f'<{node.tag}>{tmp}</{node.tag}>'


