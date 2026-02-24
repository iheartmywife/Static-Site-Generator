from generate_page import generate_page
from copystatic import copy_contents_from_a_to_b
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"



def main():
    print(f"deleting {dir_path_public}")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print(f"copying contents of {dir_path_static} to {dir_path_public}")
    copy_contents_from_a_to_b(dir_path_static, dir_path_public)

    generate_page("content/index.md", "template.html", "public/index.html")

main()