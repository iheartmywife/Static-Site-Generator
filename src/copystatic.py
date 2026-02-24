import os
import shutil

def copy_contents_from_a_to_b(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    source_contents = os.listdir(source)
    for content in source_contents:
        sub_source = os.path.join(source, content)
        sub_destination = os.path.join(destination, content)
        if os.path.isfile(sub_source):
            shutil.copy(sub_source, sub_destination)
            print(f'copied {sub_source} to {sub_destination}')
        else: #it's a directory
            copy_contents_from_a_to_b(sub_source, sub_destination)