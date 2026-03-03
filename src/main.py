from textnode import TextNode, TextType
import os
import sys

from text_to_blocks import extract_title, copy_file_paths, paste_files, empty_dir, generate_pages_recursively
def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")

    #if len(sys.argv) != 4:
    #    print("Usage: python script.py <url> <source_dir> <destination_dir>")
    #    sys.exit(1)
    #
    #url = sys.argv[1]
    #source_dir = sys.argv[2]
    #destination_dir = sys.argv[3]
    #
    #print("URL:", url)
    #print("Source:", source_dir)
    #print("Destination:", destination_dir)
    os.chdir('/home/hmon/bootdev/github.com/HmonWutt/static_site_generator/')
    static_filepaths = copy_file_paths('static')
    empty_dir('public')
    paste_files(static_filepaths,'public')
    generate_pages_recursively('content', 'template.html', 'public')
main()
print("see you later")
