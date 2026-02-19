import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def setUp(self):
        self.htmlnode1 = HTMLNode("a","this is a link to google.com", None, {"href":"https://google.com","target": "_blank"})
        self.htmlnode2 = HTMLNode("div", None, [self.htmlnode1], {})
    def test_props_to_html(self):
        self.assertEqual(f' href="https://google.com" target="_blank"', self.htmlnode1.props_to_html(), '')

    def test_children(self):
        self.assertEqual([self.htmlnode1], self.htmlnode2.children)

    def test_repr_without_children(self):
        self.assertEqual(f'HTMLNode(a,this is a link to google.com,, href="https://google.com" target="_blank")', repr(self.htmlnode1))

    def test_repr_with_children(self):
        self.assertEqual(f'HTMLNode(div,,HTMLNode(a,this is a link to google.com,, href="https://google.com" target="_blank"),)', repr(self.htmlnode2))

if __name__ == "__main__":
    unittest.main()
