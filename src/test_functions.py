# src/test_htmlnode.py

'''We testing HTML'''

import unittest

# file was originally named "functions" and it's easier to do this than rename everything
import markdown_to_node as functions

from blocktype import BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

class TestFunction(unittest.TestCase):

    '''!!!!'''

    # text_node_to_html_node(node)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_tag(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.achewood.com")
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "www.achewood.com"})

    def test_image(self):
        node = TextNode("This is an alt text", TextType.IMAGE, "www.achewood.gif")
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.achewood.gif", "alt": "This is an alt text"})



    # split_nodes_delimiter

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = functions.split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter2(self):
        node = TextNode("This is text with **some bold shit** in it, **you heard?**", TextType.TEXT)
        new_nodes = functions.split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("some bold shit", TextType.BOLD),
            TextNode(" in it, ", TextType.TEXT),
            TextNode("you heard?", TextType.BOLD)]

        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is a perfectly genteel sentence.", TextType.TEXT)
        new_nodes = functions.split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected_nodes = [node]
        self.assertEqual(expected_nodes, new_nodes)

    def test_split_nodes_odd_delimiter(self):
        node = TextNode("This is text with _one italic delimiter", TextType.TEXT)
        with self.assertRaises(
            ValueError, msg="Invalid Markdown syntax. Odd number of delimiters found"):
            functions.split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_split_nodes_odd_delimiter2(self):
        node = TextNode("this is _text_ with _three italic delimiters", TextType.TEXT)

        with self.assertRaises(
            ValueError, msg="Invalid Markdown syntax. Odd number of delimiters found"):
            functions.split_nodes_delimiter([node], "_", TextType.ITALIC)



    # split_nodes_image

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]

        self.assertListEqual(expected_nodes, new_nodes)



    # split_nodes_link

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,)
        new_nodes = functions.split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]

        self.assertListEqual(new_nodes, expected_nodes)



    # extract_markdown_images

    def test_extract_images(self):
        text = '''
        This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)
        '''
        expected_list = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]

        self.assertListEqual(functions.extract_markdown_images(text), expected_list)

    def test_extract_images2(self):
        matches = functions.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_with_links(self):
        matches = functions.extract_markdown_images(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png) AND a [link](https://www.boot.dev)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



    # extract_markdown_links

    def test_extract_links(self):
        matches = functions.extract_markdown_links(
            "Link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        )
        expected_list = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com")
            ]

        self.assertListEqual(expected_list, matches)

    def test_extract_links_with_images(self):
        matches = functions.extract_markdown_links(
            "Link [to boot dev](https://www.boot.dev) and ![here's a gif](https://www.youtube.gif)"
        )
        expected_list = [("to boot dev", "https://www.boot.dev")]

        self.assertListEqual(expected_list, matches)



    # text_to_text_nodes

    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        actual_output = functions.text_to_text_nodes(text)
        expected_output = [
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

        self.assertEqual(actual_output, expected_output)

    def test_text_to_text_nodes_nested_text(self):
        text = "This is **bold text with _nested italics_ in it**, that's crazy"

        actual_output = functions.text_to_text_nodes(text)
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text with _nested italics_ in it", TextType.BOLD),
            TextNode(", that's crazy", TextType.TEXT),
        ]

        self.assertEqual(actual_output, expected_output)



    # markdown_to_blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = functions.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    # block_to_block_type
    def test_block_to_block_type_heading(self):
        block = "### This is a header"
        actual_result = functions.block_to_block_type(block)
        expected_result = BlockType.HEADING

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_code(self):
        block = "```\nThis is code```"
        actual_result = functions.block_to_block_type(block)
        expected_result = BlockType.CODE

        self.assertEqual(actual_result, expected_result)

    def test_block_to_block_type_quote(self):
        block = "> This is a paragraph\n> of quotes\n> from a newspaper <>"
        actual_result = functions.block_to_block_type(block)

        self.assertEqual(actual_result, BlockType.QUOTE)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This\n2. Is\n3. An\n4. Ordered\n5. List of 6."
        actual_result = functions.block_to_block_type(block)

        self.assertEqual(actual_result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_unordered_list(self):
        block = "- This\n- Is\n- An\n- -Unordered-\n- List"
        actual_result = functions.block_to_block_type(block)

        self.assertEqual(actual_result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is a regular damn paragraph"
        actual_result = functions.block_to_block_type(block)

        self.assertEqual(actual_result, BlockType.PARAGRAPH)


    # markdown_to_html_node helpers

    def test_make_children(self):
        nodes = [
            TextNode("This is text with a ", TextType.TEXT)
            ]

        expected_result = [LeafNode(None, "This is text with a ", None)]
        actual_result = functions.make_children(nodes)

        self.assertEqual(expected_result, actual_result)

    def test_text_to_children(self):
        text = "This is another paragraph with _italic_ text and `code` here"
        actual_children = functions.text_to_children(text)
        expected_children = [
            LeafNode(None, "This is another paragraph with ", None),
            LeafNode("i", "italic", None),
            LeafNode(None, " text and ", None),
            LeafNode("code", "code", None),
            LeafNode(None, " here", None)
            ]

        self.assertEqual(expected_children, actual_children)

    def test_convert_heading(self):
        text = "# This is a heading\n# And this is a second line of the heading"
        actual_tag, actual_children = functions.convert_heading(text)

        expected_tag = "h1"
        expected_children = [
                LeafNode(None, "This is a heading\nAnd this is a second line of the heading")
                ]

        self.assertEqual(actual_tag, expected_tag)
        self.assertEqual(actual_children, expected_children)

    def test_convert_code(self):
        text = "```\ncode\n```"

        expected = [LeafNode("code", "code\n")]
        actual = functions.convert_codeblock(text)

        self.assertEqual(expected, actual)



    # markdown_to_html_node

    def test_heading(self):
        md = "# This is a heading\n# And this is a second line of the heading"
        node = functions.markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>This is a heading\nAnd this is a second line of the heading</h1></div>"
        )

    def test_convert_quote_simplified(self):
        text = '''> This is a quote block\n> > With nested quotes!\n> > > Quoteception!\n> Crazy, right?'''

        actual = functions.convert_quote(text)
        expected = [LeafNode(
                None, 
                "This is a quote block\n> With nested quotes!\n> > Quoteception!\nCrazy, right?", 
                None
                )]

        self.assertEqual(expected, actual)

    def test_convert_list(self):
        unordered_list = "- This is item 1\n- This is item 2\n- This is item 3"

        ordered_list = "1. This is item 1\n2. This is item 2\n3. This is item 3"

        actual_ul = functions.convert_list(unordered_list, "ul")
        actual_ol = functions.convert_list(ordered_list, "ol")

        expected_ul = [
                ParentNode("li", [LeafNode(None, "This is item 1", None)], None),
                ParentNode("li", [LeafNode(None, "This is item 2", None)], None),
                ParentNode("li", [LeafNode(None, "This is item 3", None)], None)
                ]

        expected_ol = [
                ParentNode("li", [LeafNode(None, "This is item 1", None)], None),
                ParentNode("li", [LeafNode(None, "This is item 2", None)], None),
                ParentNode("li", [LeafNode(None, "This is item 3", None)], None)
                ]

        self.assertEqual(expected_ul, actual_ul)
        self.assertEqual(expected_ol, actual_ol)

    def test_image(self):
        md = "Here is an image: ![alt text](https://i.imgur.com/zjjcJKZ.png)"

        expected = ParentNode(
            "div", 
            [
                ParentNode(
                    "p", 
                    [
                        LeafNode(None, "Here is an image: ", None),
                        LeafNode(
                            "img",
                            "",
                            {
                                "src": "https://i.imgur.com/zjjcJKZ.png",
                                "alt": "alt text"
                            }
                        )
                    ],
                    None)
            ],
            None)

        actual = functions.markdown_to_html_node(md)
        self.assertEqual(expected, actual)

    def test_link(self):
        md = "This is a [link to boot dev](https://www.boot.dev) in a sentence."

        expected = '<div><p>This is a <a href="https://www.boot.dev">link to boot dev</a> in a sentence.</p></div>'

        node = functions.markdown_to_html_node(md)
        actual = node.to_html()
        self.assertEqual(expected, actual)

    # markdown_to_html_node

    def test_heading(self):
        md = "# This is a heading\n# And this is a second line of the heading"

        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading\nAnd this is a second line of the heading</h1></div>"
        )

    def test_paragraphs(self):
        md = "This is **bolded** paragraph text in a p tag here\n\nThis is another paragraph with _italic_ text and `code` here\n\n"

        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = '''
```
This is text that _should_ remain
the **same** even with inline stuff
```
'''

        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote_simple(self):
        md = '''> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien'''

        expected = '<div><blockquote>"I am in fact a Hobbit in all but size."\n\n-- J.R.R. Tolkien</blockquote></div>'

        node = functions.markdown_to_html_node(md)
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_unordered_list(self):
        md = "- This is item 1\n- This is item 2\n- This is item 3"

        expected = "<div><ul><li>This is item 1</li><li>This is item 2</li><li>This is item 3</li></ul></div>"

        node = functions.markdown_to_html_node(md)
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_ordered_list(self):
        md = "1. This is item 1\n2. This is item 2\n3. This is item 3"

        expected = "<div><ol><li>This is item 1</li><li>This is item 2</li><li>This is item 3</li></ol></div>"

        node = functions.markdown_to_html_node(md)
        actual = node.to_html()
        self.assertEqual(expected, actual)

    # def test_blockquote_complex(self):
    #     md = "> This is a quote block\n> > With nested quotes!\n> > > Quoteception!\n> Crazy!"

    #     html = '''
    #     <blockquote>This is a quote block<blockquote>With nested quotes!<blockquote>Quoteception!</blockquote></blockquote>Crazy, right?</blockquote>
    #     '''

    #     node = functions.markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(md, html)
