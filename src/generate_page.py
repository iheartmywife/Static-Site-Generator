import os

from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        tmp = f.read()

    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)

    final_output = tmp.replace(f"{{{{ Content }}}}", html, 1).replace(f"{{{{ Title }}}}", title, 1)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_output)
    
