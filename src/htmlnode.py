class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # An HTMLNode without a tag will just render as raw text
        self.value = value # An HTMLNode without a value will be assumed to have children
        self.children = children # An HTMLNode without children will be assumed to have a value
        self.props = props # An HTMLNode without props simply won't have any attributes
    
    def to_html(self):
        raise NotImplementedError("Not Implemented")
    
    def props_to_html(self):
        html_string = ""
        if self.props is not None:
            for prop in self.props.keys():
                html_string += (f' {prop}=\"{self.props[prop]}\"')
        return html_string
    
    def __repr__(self):
        return f'tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops = {self.props}'
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag")
        if self.children is None:
            raise ValueError("no children found")
        
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        to_html_string = opening_tag
        for child in self.children:
            to_html_string += (f'{child.to_html()}')
        to_html_string += (f'{closing_tag}')
        
        return to_html_string