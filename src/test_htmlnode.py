import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "some text here", [], {"href": "https://www.google.com", 
    "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_not_props(self):
        node = HTMLNode("h1", "some text here", [])
        self.assertEqual(node.props_to_html(), "")

    def test_not_tag(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)



class TestLeafNode(unittest.TestCase):
    def test_to_html_with_props(self):
        node = LeafNode(tag="h1", value="some text here", props={"href": "https://www.google.com", 
    "target": "_blank"})

        self.assertEqual(node.to_html(), '<h1 href="https://www.google.com" target="_blank">some text here</h1>')

    def test_to_html(self):
        node = LeafNode(tag="h1", value="some text here")

        self.assertEqual(node.to_html(), '<h1>some text here</h1>')

    def test_no_tag(self):
        node = LeafNode("fartbox baby")
        self.assertEqual(node.to_html(), "fartbox baby")

class TestParentNode(unittest.TestCase):
    def test_parent_two_children(self):
        node = ParentNode(tag="h1", children=[LeafNode(tag="h2", value="first child"), LeafNode(tag="h3", value="second child")] )

        self.assertEqual(node.to_html(), '<h1><h2>first child</h2><h3>second child</h3></h1>')

    def test_nested_parents(self):
        node = ParentNode(tag="h1", children=[ParentNode(tag="h1", children=[LeafNode(tag="h2", value="first child"), LeafNode(tag="h3", value="second child")] ),LeafNode(tag="h2", value="first child"), LeafNode(tag="h3", value="second child")] )

        self.assertEqual(node.to_html(), '<h1><h1><h2>first child</h2><h3>second child</h3></h1><h2>first child</h2><h3>second child</h3></h1>')

    def test_no_tag(self):
        node = ParentNode(children=[ParentNode(tag="h1", children=[LeafNode(tag="h2", value="first child"), LeafNode(tag="h3", value="second child")] ),LeafNode(tag="h2", value="first child"), LeafNode(tag="h3", value="second child")] )

        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode(tag="h1",children=None)

        self.assertRaises(ValueError, node.to_html)



    
if __name__ == "__main__":
    unittest.main()