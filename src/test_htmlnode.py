# src/test_htmlnode.py

'''We testing HTMNodes'''

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})

        converted = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(converted, expected)


    def test_repr(self):
        node = HTMLNode(
            tag="h1",
            value="Some text",
            children=[
                HTMLNode(tag="p", value="Child paragraph"),
                HTMLNode(tag="a", value="A link")
                ],
            props={"href": "https://www.google.com", "target": "_blank"}
            )

        expected = "HTMLNode(h1, Some text, [HTMLNode(p, Child paragraph, None, None), HTMLNode(a, A link, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
        actual = str(node)

        self.assertEqual(expected, actual)


    def test_repr2(self):
        node = HTMLNode()

        expected = "HTMLNode(None, None, None, None)"
        actual = str(node)

        self.assertEqual(expected, actual)


    # LeafNode

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    # ParentNode

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(
            ValueError, msg="ValueError: All parent nodes must have at least one child.")

    def test_to_html_one_child(self):
        child_node = LeafNode("p", "Only child")
        parent_node = ParentNode("section", [child_node])
        self.assertEqual(parent_node.to_html(), "<section><p>Only child</p></section>")

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "Child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, msg="ValueError: All parent nodes must have a tag.")

    def test_to_html_crazy_quote(self):
        crazy_quote = ParentNode(
            "blockquote",
            [
                LeafNode(None,"This is a quote block",None),
                ParentNode(
                    "blockquote",
                    [
                        LeafNode(None, "With nested quotes!", None),
                        ParentNode(
                            "blockquote",
                            [
                                LeafNode(None, "Quoteception!", None)
                            ],
                            None)
                    ],
                    None),
                LeafNode(None, "Crazy, right?", None)
            ],
            None)

        expected = "<blockquote>This is a quote block<blockquote>With nested quotes!<blockquote>Quoteception!</blockquote></blockquote>Crazy, right?</blockquote>"
        actual = crazy_quote.to_html()

        self.assertEqual(expected, actual)

    def test_repr_parent(self):
        child_node = LeafNode("p", "Child")
        parent_node = ParentNode("div", [child_node])

        expected = "ParentNode(div, [LeafNode(p, Child, None)], None)"
        actual = str(parent_node)

        self.assertEqual(expected, actual)
