from markdown_blocks import markdown_to_html_node, extract_title
from htmlnode import * 

import os
import shutil

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            html_filename = dest_path.replace(".md", ".html")
            generate_page(from_path, template_path, html_filename)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template__path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template__path}")

    original_markdown = grab_file_contents(from_path)
    template = grab_file_contents(template__path)
    html_node = markdown_to_html_node(original_markdown)
    generated_html = html_node.to_html() 
    
    

    page_title = extract_title(original_markdown)

    new_html_page = template.replace("{{ Content }}", generated_html).replace("{{ Title }}", page_title)
    
    with open(dest_path,'w+', encoding="utf-8") as file:
        file.write(new_html_page)


def grab_file_contents(path):
    with open(path, encoding="utf-8") as file:
        read_data = file.read()
        return read_data