import unittest
import os
import json
from jenkins_log_parser.buildlog import BuildLog


class TestLogNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.buildlog = BuildLog(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)
                ),
                "input_data"
            )
        )
        cls.buildlog.collect_nodes()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_zip(self):
        # download zip from remote source!
        # push the path in and see what happens
        print("Currently not implemented")

    def test_node_collect(self):
        nodes = self.buildlog.nodes
        print("__ nodes: %s" % len(nodes))
        self.assertEqual(995, len(nodes))
        self.assertTrue(5 in nodes.keys())
        self.assertTrue(1003 in nodes.keys())

    def test_node_log_collect(self):
        self.buildlog.collect_nodes_logs()

        nodes = self.buildlog.nodes

        self.assertEqual(4046, nodes.get(5).indices[0].get("start"))
        self.assertEqual(4111, nodes.get(5).indices[0].get("end"))
        self.assertEqual(0, len(nodes.get(4).indices))
        self.assertEqual(143992, nodes.get(141).indices[0].get("start"))
        self.assertEqual(144121, nodes.get(141).indices[0].get("end"))

    def test_tree(self):
        tree = self.buildlog.create_tree()
        print(json.dumps(tree, indent=4))
        self.assertEqual(tree.get(4), [5])
        self.assertEqual(tree.get(3), [4])
        self.assertEqual(tree.get(119), [126, 127, 128, 129, 130, 131, 132])
