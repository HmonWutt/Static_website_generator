from textnode import TextNode, TextType
import os

from text_to_blocks import extract_title, copy_files, paste_files, empty_dir, generate_page
def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")
    os.chdir('/home/hmon/bootdev/github.com/HmonWutt/static_site_generator/')
    filepaths = copy_files('static')
    empty_dir('public')
    paste_files(filepaths,'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')
main()
print("see you later")
