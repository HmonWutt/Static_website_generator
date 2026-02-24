from textnode import TextNode, TextType
import os
import shutil
from pathlib import Path
def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")
    os.chdir('/home/hmon/bootdev/github.com/HmonWutt/static_site_generator/')
    filepaths = copy_files('static')
    empty_dir('public')
    paste_files(filepaths,'public')
    #print(text_node)

def copy_files(src_dir):
    if not os.path.exists(src_dir):
        raise Exception("source path not valid")
    if os.path.isfile(src_dir):
        return src_dir
    return helper_copy_files(src_dir,[])

def helper_copy_files(path,file_paths):
    if os.path.isfile(path):
        file_paths.append(path)
        print("src: ",path)
        return file_paths
    sub_dirs = os.listdir(path) 
    for sub_dir in sub_dirs:
        joined_path = os.path.join(path,sub_dir)
        helper_copy_files(joined_path, file_paths)
    return file_paths

def paste_files(filepaths, destination_dir):
    for filepath in filepaths:
        src_path = os.path.join(*filepath.split(os.sep)[1:])
        dest_path = os.path.join(destination_dir,src_path)
        dir = os.path.dirname(dest_path)
        os.makedirs(dir,exist_ok=True)
        shutil.copy(filepath,dest_path)
        print("dest: ",dest_path)

def empty_dir(dir):
    dir = Path(dir)
    for item in dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
main()
print("see you later")
