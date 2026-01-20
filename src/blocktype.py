# src/blocktype.py

'''BlockType class and related materials'''

from enum import Enum

class BlockType(Enum):

    '''Catalog of different types of block-level text'''

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
