import unittest
import os
from jenkins_log_parser.lognode import LogNode


class TestLogNode(unittest.TestCase):
    def setUp(self):
        os.chdir(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)
                ),
                "input_data"
            )
        )

    def tearDown(self):
        pass

    def test_init(self):
        lognode = LogNode(5)
        self.assertEqual(lognode.node_no, 5)
        self.assertEqual(len(lognode.indices), 0)

    def test_xml_content_retrieval(self):
        lognode = LogNode(5)
        print("__ %s" % lognode.get_node_class())
        self.assertEqual("cps.n.StepAtomNode", lognode.get_node_class())
        print("__ %s" % lognode.get_node_descriptorId())
        self.assertEqual(
            "org.jenkinsci.plugins.workflow.steps.EchoStep",
            lognode.get_node_descriptorId())
        print("__ %s" % lognode.get_parent_id())
        self.assertEqual(
            4,
            lognode.get_parent_id())
        print("__ %s" % lognode.get_step())
        self.assertEqual(
            "EchoStep",
            lognode.get_step())
        print("__ %s" % lognode.get_path_text("node/descriptorId"))
        self.assertEqual(
            "org.jenkinsci.plugins.workflow.steps.EchoStep",
            lognode.get_path_text("node/descriptorId"))

    def test_get_log(self):
        lognode = LogNode(5)
        lognode.set_log_file("log")
        lognode.add_index(4046, 4111)
        print("__ %s" % lognode.get_log())
        self.assertEqual(
            "<replace-with-expected-strings>",  # noqa
            lognode.get_log())
