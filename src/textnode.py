# src/textnode.py

'''Intermediary classes for translation of Markdown to HTML'''

from enum import Enum

class TextType(Enum):

    '''Catalog of different types of inline text
    To be used in conjunction with TextNode objects
    NAMES accessed by user via .name
    "values" accessed by user via .value'''

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():

    '''For handling of web text
    Formatting concerns are stored as object properties'''

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type # TextType.NAME
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type.name == other.text_type.name
                and self.url == other.url)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
