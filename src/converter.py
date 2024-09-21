import re

from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # already split
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_node_text = node.text.split(delimiter)

        if len(split_node_text) % 2 == 0:
            raise Exception("No matching delimiter found")
        
        split_node =[]
        for idx, text in enumerate(split_node_text):        
            if idx % 2 == 1:
                split_node.append(TextNode(text=text, text_type=text_type))
            else: 
                split_node.append(TextNode(text=text, text_type=text_type_text))

        new_nodes.extend(split_node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=text_type_text))
            new_nodes.append(
                TextNode(
                    text=image[0],
                    text_type=text_type_image,
                    url=image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text, text_type=text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=text_type_text))
            new_nodes.append(TextNode(text=link[0], text_type=text_type_link, url=link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text, text_type=text_type_text))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def text_to_textnodes(text):
    initial_node = TextNode(text=text, text_type=text_type_text)
    split_by_image = split_nodes_image([initial_node])
    split_by_links = split_nodes_link(split_by_image)
    split_by_bold = split_nodes_delimiter(split_by_links, "**", text_type_bold)
    split_by_italic = split_nodes_delimiter(split_by_bold, "*", text_type_italic)
    split_by_italic_again = split_nodes_delimiter(split_by_italic, "_", text_type_italic)
    split_by_code = split_nodes_delimiter(split_by_italic_again, "`", text_type_code)
    

    return split_by_code