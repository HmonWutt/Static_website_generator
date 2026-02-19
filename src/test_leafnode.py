import unittest
from leafnode import LeafNode
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "some value",{"href":"https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">some value</a>')


if __name__ == "__main__":
    unittest.main()
