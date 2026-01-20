# src/htmlnode.py

'''HTML counterpart to textnode'''

class HTMLNode():

    '''For handling of HTML'''

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value

        if children:
            self.children = []
            for child in children:
                self.children.append(child)
        else:
            self.children = None

        if props:
            self.props = {}
            for prop in props:
                self.props[prop] = props[prop]
        else:
            self.props = None

    def __eq__(self, other):
        return (self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {repr(self.children)}, {str(self.props)})'

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        '''
        {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        ---
        href="https://www.google.com" target="_blank"
        '''

        converted = ""
        if self.props:
            for key in self.props:
                converted += f' {key}="{self.props[key]}"'
        return converted

class LeafNode(HTMLNode):

    '''For handling of HTML leaf nodes (no children)'''

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        return (self.tag == other.tag
                and self.value == other.value
                and self.props == other.props)

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {str(self.props)})'

class ParentNode(HTMLNode):

    '''Our new ParentNode class will handle the nesting of HTML nodes inside of one another.
    Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.'''

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")

        if not self.children:
            raise ValueError("All parent nodes must have at least one child.")

        converted_html = f"<{self.tag}>"
        for child in self.children:
            converted_html += child.to_html()
        return converted_html + f"</{self.tag}>"

    def __eq__(self, other):
        return (self.tag == other.tag
                and self.children == other.children
                and self.props == other.props)

    def __repr__(self):
        return f'ParentNode({self.tag}, {repr(self.children)}, {str(self.props)})'
