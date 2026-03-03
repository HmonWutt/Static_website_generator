from textnode import TextNode, TextType
import os
import sys

from text_to_blocks import extract_title, copy_file_paths, paste_files, empty_dir, generate_pages_recursively
def main():
    if len(sys.argv) != 5:
        print("Usage: python3 src/main.py <your github page url> <static files source directory> <md source directory> <destination directory>")
        sys.exit(1)
    
    basepath = sys.argv[1]
    static_src_dir = sys.argv[2]
    md_src_dir = sys.argv[3]
    dest_dir = sys.argv[4]
    print("Github pages url:", basepath)
    static_filepaths = copy_file_paths(static_src_dir)
    empty_dir(dest_dir)
    paste_files(static_filepaths,dest_dir)
    generate_pages_recursively(md_src_dir, 'template.html', dest_dir,basepath)
main()
