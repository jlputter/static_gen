import unittest

from textnode import TextNode
from htmlnode import *

def main():
    text_node = TextNode("fart box in a *juice*  *box*", "text", "www.getlaid.com")
    text_node2 = TextNode("*juice*  *box*", "text", "www.getlaid.com")


main()