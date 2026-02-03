class HTMLNode:
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag # An HTMLNode without a tag will just render as raw text
        self.value = value # An HTMLNode without a value will be assumed to have children
        self.children = children # An HTMLNode without children will be assumed to have a value
        self.props = props # An HTMLNode without props simply won't have any attributes
    
    def to_html(self):
        raise NotImplementedError("Not Implemented")
    
    def props_to_html(self):
        html_string = ""
        if self.props is None:
            return html_string
        else:
            for prop in self.props.keys():
                html_string.append(f' {prop}=\"{self.props[prop]}\"')
        return html_string
    
    def __repr__(self):
        return f'tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops = {self.props}'