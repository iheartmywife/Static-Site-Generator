from generate_page import generate_pages_recursive
from copystatic import copy_contents_from_a_to_b
import os
import shutil
import sys

dir_path_docs = "./docs"
dir_path_static = "./static"
dir_path_content = "./content"
template_path = "./template.html"



def main():
    print(f"deleting {dir_path_docs}")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    if sys.argv:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print(f"copying contents of {dir_path_static} to {dir_path_docs}")
    copy_contents_from_a_to_b(dir_path_static, dir_path_docs)

    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)

main()