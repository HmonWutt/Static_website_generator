class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet")

    def props_to_html(self):
        if not self.props:
            return None
        result = ""
        for key, value in self.props.items():
            result+=f'{key}="{value}" '
        return result 

    def __repr__(self):
        children_list = ""
        if not self.children:
            children_list+="None"
        else:
            for each in self.children:
                children_list+=repr(each)
        return f"HTMLNode({self.tag}, {self.value}, {children_list}, {self.props_to_html()})"
    
