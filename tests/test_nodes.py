import sys
import unittest

#import nodes
from src.nodes import TreeEditor, Node

class TestNode(unittest.TestCase):
    def test_creating_node(self):
        new =  Node(name="test")
        self.assertEqual(new.sub_nodes, [], "Should Empty Be Empty")
