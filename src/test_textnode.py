import unittest

from htmlnode import LeafNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)
from converter import *


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


class TestTextToLeafFunctions(unittest.TestCase):
    def test_eq_italic(self):
        node = TextNode(text="This is a text node", text_type=text_type_italic)
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.value, "This is a text node")
        self.assertEqual(new_node.tag, "i")

    def test_eq_bold(self):
        node = TextNode(text="This is a text node 2", text_type=text_type_bold)
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.value, "This is a text node 2")
        self.assertEqual(new_node.tag, "b")

    def test_eq_image(self):
        node = TextNode("This is a text node 2", text_type_image, url="www.fartbox.com")
        new_node = text_node_to_html_node(node)
        self.assertEqual(new_node.props_to_html(), ' src="www.fartbox.com" alt="This is a text node 2"')


class TestTextNodeSplitFunctions(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is a **text** node", text_type_text)
        split_node = split_nodes_delimiter([node], "**", text_type_bold)
        print(split_node)
        self.assertEqual(split_node, [TextNode("This is a ", text_type_text), TextNode("text", text_type_bold), TextNode(" node", text_type_text)])

    def test_double_split_italic(self):
        node = TextNode("This is a *text* *node*", text_type_text)
        split_node = split_nodes_delimiter([node], "*", text_type_italic)
        print(split_node)
        self.assertEqual(split_node, [TextNode("This is a ", text_type_text), TextNode("text", text_type_italic), TextNode(" ", text_type_text), TextNode("node", text_type_italic), TextNode("", text_type_text)])

    def test_double_input_node_code(self):
        node = TextNode("This is a `text` node", text_type_text)
        node2 = TextNode("This is a `text` `node`", text_type_text)
        split_node = split_nodes_delimiter([node, node2], "`", text_type_code)
        print(split_node)
        self.assertEqual(split_node, [TextNode("This is a ", text_type_text), TextNode("text", text_type_code), TextNode(" node", text_type_text), TextNode("This is a ", text_type_text), TextNode("text", text_type_code), TextNode(" ", text_type_text), TextNode("node", text_type_code), TextNode("", text_type_text)])

    def test_no_closing(self):
        self.assertRaises(Exception, split_nodes_delimiter)

    def test_image_extract(self):
        test_text="the moon in ![your eyes](shines bright like a diamond)"
        self.assertEqual([('your eyes', 'shines bright like a diamond')], extract_markdown_images(test_text))

    def test_image_extract_twice(self):
        test_text="the moon in ![your eyes](shines bright like a diamond) ![your eyes](shines bright like a diamond)"
        self.assertEqual([('your eyes', 'shines bright like a diamond'), ('your eyes', 'shines bright like a diamond')], extract_markdown_images(test_text))

    def test_link_extract(self):
        test_text="the moon in [your eyes](shines bright like a diamond) "
        self.assertEqual([('your eyes', 'shines bright like a diamond')], extract_markdown_links(test_text))

    def test_link_extract_twice(self):
        test_text="the moon in [your eyes](shines bright like a diamond) [your eyes](shines bright like a diamond)"
        self.assertEqual([('your eyes', 'shines bright like a diamond'), ('your eyes', 'shines bright like a diamond')], extract_markdown_links(test_text))

    def test_link_extract(self):
        test_text="the moon in [your eyes](shines bright like a diamond) "
        self.assertEqual([('your eyes', 'shines bright like a diamond')], extract_markdown_links(test_text))

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
    
    # def test_split_
if __name__ == "__main__":
    unittest.main()