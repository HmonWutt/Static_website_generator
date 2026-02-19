import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_create(self):
        htmlnode1 = HTMLNode("a","this is a link to google.com", None, {"href":"https://google.com","target": "_blank"})
        htmlnode2 = HTMLNode("div", None, [htmlnode1], {})
        self.assertEqual(f'href="https://google.com" target="_blank" ', htmlnode1.props_to_html(), '')
        self.assertEqual([htmlnode1], htmlnode2.children)
        self.assertEqual(f'HTMLNode(a, this is a link to google.com, , href="https://google.com" target="_blank" )', repr(htmlnode1))
