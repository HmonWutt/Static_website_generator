from textnode import TextNode, TextType
import os
import sys

from text_to_blocks import extract_title, copy_file_paths, paste_files, empty_dir, generate_pages_recursively
def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")

    if len(sys.argv) != 2:
        print("Usage: python script.py <url> <source_dir> <destination_dir>")
        sys.exit(1)
    
    basepath = sys.argv[1]
    print("Basepath:", basepath)
    static_filepaths = copy_file_paths('static')
    empty_dir('docs')
    paste_files(static_filepaths,'docs')
    generate_pages_recursively('content', 'template.html', 'docs',basepath)
main()
print("see you later")
