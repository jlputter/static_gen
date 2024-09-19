from htmlnode import LeafNode




class TextNode():

    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"
    

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
         return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextNode.text_type_text:
            return LeafNode(text_node.text)
        case TextNode.text_type_bold:
            return LeafNode(text_node.text, tag="b")
        case TextNode.text_type_italic:
            return LeafNode(text_node.text, tag="i")
        case TextNode.text_type_code:
            return LeafNode(text_node.text, tag="code")
        case TextNode.text_type_link:
            return LeafNode(text_node.text, "a")
        case TextNode.text_type_image:
            return LeafNode("", tag="img", props={"src": text_node.url, "alt": text_node.text})
    raise Exception("Invalid HTML tag")