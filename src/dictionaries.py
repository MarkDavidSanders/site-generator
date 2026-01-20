# src/dictionaries.py

'''Global dicts live here, maybe other global variables in the future'''

# text_type -> html tag
inline_dict = {
    "TEXT": None,
    "BOLD": "b",
    "ITALIC": "i",
    "CODE": "code",
    "LINK": "a",
    "IMAGE": "img"
}

# block_type -> html tag
block_dict = {
    "PARAGRAPH": "p",
    "HEADING": "h",  # will add level later
    "CODE": "pre",
    "QUOTE": "blockquote",
    "UNORDERED_LIST": "ul",
    "ORDERED_LIST": "ol"
}