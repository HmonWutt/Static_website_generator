from textnode import TextNode, TextType


def main():
    text_node = TextNode("hello world", TextType.BOLD, "www.dummy.com")
    print(text_node)


main()
print("see you later")
