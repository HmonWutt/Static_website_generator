from textnode import TextNode, TextType
import os

from text_to_blocks import extract_title, copy_file_paths, paste_files, empty_dir, generate_pages_recursively
def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")
    os.chdir('/home/hmon/bootdev/github.com/HmonWutt/static_site_generator/')
    static_filepaths = copy_file_paths('static')
    empty_dir('public')
    paste_files(static_filepaths,'public')
    generate_pages_recursively('content', 'template.html', 'public')
main()
print("see you later")
