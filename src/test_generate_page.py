# src/test_generate_page.py

'''We testing HTML'''

import unittest

import generate_page
import markdown_to_node

from blocktype import BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

class TestFunction(unittest.TestCase):

    '''!!!!'''

    def test_extract_title(self):
        markdown = "# Header"
        markdown2 = "# Header\n# Header"
        markdown3 = "## Subheader\n\n# Real header"
        markdown4 = "Ain't shit"

        header = generate_page.extract_title(markdown)
        header2 = generate_page.extract_title(markdown2)
        header3 = generate_page.extract_title(markdown3)

        self.assertEqual(header, "Header")
        self.assertEqual(header2, "Header\nHeader")
        self.assertEqual(header3, "Real header")
        with self.assertRaises(ValueError):
            generate_page.extract_title(markdown4)
