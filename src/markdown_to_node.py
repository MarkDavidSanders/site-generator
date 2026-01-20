# src/markdown_to_node.py

'''
Functions pertaining to HTMLNode creation and markdown-to-HTML conversion
'''

import re

from blocktype import BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

from dictionaries import inline_dict, block_dict


def text_node_to_html_node(text_node):
    '''
    leaf_node.value = text_node.text
    leaf_node.tag = text_node.text_type

    Image.value goes to props as alt text
    Image.text = ""

    leaf_node.props:
        - Images: text_node.url and text_node.text
        - Links: text_node.url
        None for all other types
    '''

    try:
        tag = inline_dict[text_node.text_type.name]
    except Exception as exc:
        raise ValueError("Invalid TextType provided.") from exc

    if text_node.text_type.name == "IMAGE":
        value = ""
        props = {"src": f"{text_node.url}",
                    "alt": f"{text_node.text}"}

    elif text_node.text_type.name == "LINK":
        value = text_node.text
        props = {"href": f"{text_node.url}"}

    else:
        value = text_node.text
        props = None

    return LeafNode(tag=tag, value=value, props=props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    TextNode("This is text with a `code block` word", TextType.TEXT)

    becomes
    
    [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
    ]
    '''

    if not old_nodes:
        return []
    new_nodes = []

    for node in old_nodes:
        converted_nodes = []

        if node.text_type.name != "TEXT" or delimiter not in node.text:
            new_nodes.append(node)

        elif node.text.count(delimiter) % 2 == 1:
            raise ValueError("Invalid Markdown syntax. Odd number of delimiters found")

        else:
            converted_text = node.text.split(delimiter)

            for phrase in converted_text:
                if phrase in converted_text[1::2]:
                    converted_nodes.append(TextNode(phrase, text_type))
                elif phrase != "":
                    converted_nodes.append(TextNode(phrase, TextType.TEXT))

            new_nodes.extend(converted_nodes)

    return new_nodes

def extract_markdown_images(text):
    '''
    Takes raw markdown text and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images.
    '''

    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    '''Like extract_markdown_images, but with links.'''

    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    '''Same as split_nodes_delimiter but for images.'''

    if not old_nodes:
        return []
    new_nodes = []

    for node in old_nodes:
        converted_nodes = []

        if node.text_type.name != "TEXT":
            new_nodes.append(node)

        else:
            image_pairs = extract_markdown_images(node.text)
            converted_text = re.split(r"\!\[(.*?)\]\(.*?\)", node.text)
            # URLs are not included in converted_text

            for phrase in converted_text:
                if any(phrase in pair for pair in image_pairs):
                    url = next(u for (a, u) in image_pairs if a == phrase)
                    converted_nodes.append(TextNode(phrase, TextType.IMAGE, url))
                elif phrase != "":
                    converted_nodes.append(TextNode(phrase, TextType.TEXT))

            new_nodes.extend(converted_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    '''Splits nodes for links.'''

    if not old_nodes:
        return []
    new_nodes = []

    for node in old_nodes:
        converted_nodes = []

        if node.text_type.name != "TEXT":
            new_nodes.append(node)

        else:
            link_pairs = extract_markdown_links(node.text)
            converted_text = re.split(r"(?<!\!)\[(.*?)\]\(.*?\)", node.text)
            # URLs are not included in converted_text

            for phrase in converted_text:
                if any(phrase in pair for pair in link_pairs):
                    url = next(u for (a, u) in link_pairs if a == phrase)
                    converted_nodes.append(TextNode(phrase, TextType.LINK, url))
                elif phrase != "":
                    converted_nodes.append(TextNode(phrase, TextType.TEXT))

            new_nodes.extend(converted_nodes)

    return new_nodes

def text_to_text_nodes(text):
    '''
    Converts inline markdown text to a list of TextNode objects.

    Input:
        This is **text** with an _italic_ word and a `code block`
        and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

    Output:
    [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    '''

    if not text:
        return []

    old_node = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_image(old_node)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    return new_nodes

def markdown_to_blocks(markdown):
    '''
   Input:
    ---
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item

    ```
    This is a code block
    ```
    ---

    Output:
    [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
        "- This is the first list item in a list block\n- This is an item\n- This is another item",
        "```\nThis is a code block\n```"
    ]
    '''

    if not markdown:
        return []

    blocks = []
    for block in markdown.strip().split("\n\n"):
        if block != "":
            blocks.append(block)

    return blocks

def block_to_block_type(text):
    '''
    Takes a single block of markdown text as input.
    Returns the BlockType representing the type of block it is.
    '''

    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING

    if text.startswith("```\n") and text.endswith("```"):
        return BlockType.CODE

    lines = text.split("\n")
    is_quote = all(line.startswith(">") for line in lines)
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = all(line.startswith("- ") for line in lines)
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # walrus operator is cool, it lets you assign a variable within an expression
    is_ordered_list = all(
        (matches := re.match(r'^(\d+)\. ', line)) and int(matches.group(1)) == index
        for index, line in enumerate(lines, start=1)
        )
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# markdown_to_html_node helper functions
def make_children(nodes):
    '''Takes a list of TextNodes, returns a list of LeafNodes'''

    children = []
    for node in nodes:
        leaf = text_node_to_html_node(node)
        children.append(leaf)
    return children

def text_to_children(text):
    '''
    Returns a list of LeafNodes that represent the inline markdown.
    Works for all types. Assumes removal of block syntax.
    '''

    nodes = text_to_text_nodes(text)
    return make_children(nodes)

def convert_heading(text):
    '''Returns list of child nodes with a level-specific tag'''

    lines = text.split("\n")
    new_lines = [line.lstrip("#").lstrip() for line in lines]
    text = "\n".join(new_lines)
    nodes = text_to_text_nodes(text)
    children = make_children(nodes)

    # length diff is number of hashes + 1
    level = str(len(lines[0]) - len(new_lines[0]) - 1)
    tag = f"h{level}"

    return tag, children

def convert_codeblock(text):
    '''
    Converts code to node.
    Codeblocks don't get inline formatting so will always be a single node.
    '''

    new_text = re.sub(r"^```\n|```$", "", text.strip())
    return [text_node_to_html_node(TextNode(text=new_text, text_type=TextType.CODE))]

def convert_quote(text):
    '''
    This is a simplified version of the hashed-out function at the bottom of the script,
    which I could not quite make work after hours of trying.
    I might come back to it.
    It's probably totally unnecessary anyway, but I wanted nested quotes :(

    Returns list of children.
    '''

    lines = [line.removeprefix(">").lstrip(" ") for line in text.split("\n")]
    text = "\n".join(lines)
    nodes = text_to_text_nodes(text)
    return make_children(nodes)

def convert_list(text, tag):
    '''
    - This is the first list item in a list block
    - This is a list item
    - This is another list item

    1. This is the first list item in a list block
    2. This is a list item
    3. This is another list item

    <ul> OR <ol>
        <li>This is the first list item in a list block</li>
        <li>This is a list item</li>
        <li>This is another list item</li>
    </ul> OR <ol>
    '''

    children = []

    if tag == "ul":
        item_list = [line.removeprefix("- ") for line in text.split("\n")]
    else:  # "ol"
        item_list = [re.sub("^\\d+\\. ", "", line) for line in text.split("\n")]

    for item in item_list:
        item_children = text_to_children(item)
        children.append(ParentNode(tag="li", children=item_children))

    return children

def block_to_node(block):
    '''
    Basically a markdown conversion router.
    Calls type-specific functions as needed.
    Returns ParentNode with the appropriate tag and children.
    '''

    block_type = block_to_block_type(block)
    tag = block_dict[block_type.name]

    if block_type.name == "HEADING":
        tag, b_children = convert_heading(block) # level-specific tag
    elif block_type.name == "CODE":
        b_children = convert_codeblock(block)
    elif block_type.name == "QUOTE":
        b_children = convert_quote(block)
    elif block_type.name in ("ORDERED_LIST", "UNORDERED_LIST"):
        b_children = convert_list(block, tag)
    else: # paragraph
        b_children = text_to_children(block)

    return ParentNode(tag=tag, children=b_children)

# markdown_to_html_node
def markdown_to_html_node(markdown):
    '''
    Converts a full markdown document into a single parent HTMLNode.
    
    That one parent HTMLNode should contain many child HTMLNode objects
    representing all nested elements.
    '''
    div_children = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_node = block_to_node(block)
        div_children.append(block_node)

    div_parent = ParentNode(tag="div", children=div_children)

    return div_parent










# def convert_quote_nested(text):
#     '''
#     > This is a quote block
#     > > With nested quotes!
#     > > > Quoteception!
#     > Crazy, right?

#     <blockquote>This is a quote block<blockquote>With nested quotes!<blockquote>Quoteception!</blockquote></blockquote>Crazy, right?</blockquote>
#     '''

#     # remove first tag from each line
#     lines = [line.removeprefix("> ") for line in text.split("\n")]
#     text = "\n".join(lines)

#     # if quoteblock is entirely toplevel, we're done
#     if not any(line.startswith("> ") for line in lines):

#         return [ParentNode(tag="blockquote", children=text_to_children("\n".join(lines)[0]))]

#     # nested quotes
#     # compile next-level lines
#     nextlevel_quote = []

#     for line in lines:
#         if line.startswith("> "):
#             nextlevel_quote.append(line)
#         elif nextlevel_quote:
#             # next-level block is complete
#             break

#     # split OG lines by next-level string into two chunks
#     nextlevel_quote = "\n".join(nextlevel_quote)
#     toplevel_chunks = text.split(nextlevel_quote, 1)

#     # convert "before nextlevel" (if not empty)
#     # += parent node w/recursive children
#     # += convert "after nextlevel" (if not empty)

#     # "Before" is definitely toplevel but "After" chunk might be nested
#     before, after = toplevel_chunks[0], toplevel_chunks[1]

#     if before != "":
#         # create toplevel ParentNode starting with before
#         toplevel_node = ParentNode(tag="blockquote", children=text_to_children(before.strip()))
#         # append nextlevel ParentNode
#         toplevel_node.children.append(convert_quote(nextlevel_quote))
#     else:
#         # before is empty, start with nextlevel ParentNode
#         toplevel_node = ParentNode(tag="blockquote", children=convert_quote(nextlevel_quote))
#         if after != "":
#             if any(line.startswith("> ") for line in after.split("\n")):
#                 # recursively append after
#                 toplevel_node.children.extend(convert_quote(after))
#             else:
#                 # toplevel after, no need to recurse
#                 toplevel_node.children.extend(text_to_children(after))

#     return toplevel_node