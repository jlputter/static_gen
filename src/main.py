from textnode import TextNode
from htmlnode import *
from converter import *
from markdown_blocks import *

def main():
    test_string = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    # text_node = TextNode("fart box in a *juice*  *box*", "text", "www.getlaid.com")
    # text_node2 = TextNode("*juice*  *box*", "text", "www.getlaid.com")

    # text_extract_image = TextNode("this is fake text before the two instances ![blim](blaaaaam) skibidi skibidi ![blimo](blaaaaamo) this is some text afterwards <3", "text")
    # print(split_nodes_image([text_extract_image]) )

    # text_extract_link = TextNode("this is fake text before the two instances [blim](blaaaaam) skibidi skibidi ![blimo](blaaaaamo) this is some text afterwards <3", "text")
    # print(split_nodes_link([text_extract_link]))


    # tester =  "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    # print(text_to_textnodes(tester))
          
    print(markdown_to_blocks(test_string))



main()