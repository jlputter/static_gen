import unittest

from htmlnode import LeafNode
from textnode import (
    TextNode,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold","www.com.com")
        node2 = TextNode("This is a text node", "bold", "www.com.com")
        self.assertEqual(node,node2)

    def test_not_eq_with_missing_url(self):
        node = TextNode("This is a text node", "bold","www.com.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node,node2)

    def test_not_eq_with_different_url(self):
        node = TextNode("This is a text node", "bold","www.com.com")
        node2 = TextNode("This is a text node", "bold", "www.notthesame.com")
        self.assertNotEqual(node,node2)

    def test_not_eq_with_different_type(self):
        node = TextNode("This is a text node", "bold","www.com.com")
        node2 = TextNode("This is a text node", "italic", "www.notthesame.com")
        self.assertNotEqual(node,node2)


class TestMainFunctions(unittest.TestCase):
    def test_eq_italic(self):
        node = TextNode("This is a text node", TextNode.text_type_italic)
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.value, "This is a text node")
        self.assertEqual(new_node.tag, "i")

    def test_eq_bold(self):
        node = TextNode("This is a text node 2", TextNode.text_type_bold)
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.value, "This is a text node 2")
        self.assertEqual(new_node.tag, "b")

    def test_eq_image(self):
        node = TextNode("This is a text node 2", TextNode.text_type_image, url="www.fartbox.com")
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.props_to_html(), ' src="www.fartbox.com" alt="This is a text node 2"')


if __name__ == "__main__":
    unittest.main()