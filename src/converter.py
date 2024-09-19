from textnode import TextNode, text_type_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # already split
        if node.text_type != text_type_text:
            new_nodes.append(node)

        split_node_text = node.text.split(delimiter)
        
        if len(split_node_text) % 2 == 0:
            raise Exception("No matching delimiter found")
        
        split_node =[]

        for idx, text in enumerate(split_node_text):        
            if idx % 2 == 1:
                split_node.append(TextNode(text, text_type))
            else: 
                split_node.append(TextNode(text, text_type_text))

        new_nodes.extend(split_node)
    return new_nodes
