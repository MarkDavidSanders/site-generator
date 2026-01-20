# src/generate_page.py

'''Generates a single HTML page from markdown input'''

import os

import markdown_to_node

from copy_static import copy_static

def extract_title(markdown):
    '''Extracts h1 header from markdown file and returns as title'''
    blocks = markdown_to_node.markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith('# '):
            return "\n".join([line.lstrip("# ") for line in block.split("\n")])
    raise ValueError("No toplevel header found in markdown")

def generate_page(from_path, template_path, dest_path):
    '''
    Converts markdown file at from_path to HTML and inserts into template.
    Writes adjusted template to dest_path. Creates destination folders as needed.
    '''

    print(f">>> Generating page from {from_path} to {dest_path}")

    try:
        with open(from_path, 'r', encoding='utf-8') as f:
            markdown = f.read()
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"!!! Error reading files: {e}")
        return

    node = markdown_to_node.markdown_to_html_node(markdown)
    html_string = node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    '''
    Recursively searches content directory and generates HTML pages for any markdown file found
    '''

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith('.md'):
            rel_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, f'{rel_path[:-3]}.html')
            generate_page(item_path, template_path, dest_path)
        elif os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_dir)
