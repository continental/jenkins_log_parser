#! /usr/bin/env python3

"""
jenkins_log_processor Main module
"""

import argparse
import os
from jenkins_log_parser.buildlog import BuildLog
from jenkins_log_parser.logprocessor import LogProcessor


def main():
    """
    Main function, parsing arguments and calling the stuff.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "log_location",
        type=str
    )
    parser.add_argument(
        "-t", "--target",
        type=str,
        action="store",
        default=os.getcwd()
    )
    args = parser.parse_args()

    target_dir = os.path.realpath(args.target)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    build_log = BuildLog(args.log_location)
    nodes = build_log.collect_nodes()
    tree = build_log.create_tree()
    build_log.collect_nodes_logs()
    # walker = TreeWalker(nodes, tree)
    # current = walker.next()
    # while current is not None:
    #     node = current
    #     parents = walker.list_parents(node.node_no)
    #     p_stage = None
    #     for p in parents:
    #         if p is not None and p.get_step() == "StageStep":
    #             if p.get_path_text(
    #                 "./actions/wf.a.LabelAction/displayName"
    #             ) is not None:
    #                 p_stage = p.get_path_text(
    #                     "./actions/wf.a.LabelAction/displayName"
    #                 )
    #                 break
    #     print("{} {} {} {} {} {}".format(
    #         node.node_no,
    #         node.get_node_class(),
    #         node.get_node_descriptorId().split(".")[-1] if
    #         node.get_node_descriptorId() is not None else "None",
    #         node.get_parent_id(),
    #         walker.depth(node.node_no),
    #         p_stage
    #     ))
    #     current = walker.next()

    log_proc = LogProcessor(target_dir)

    log_proc.process(nodes, tree)


if __name__ == "__main__":
    main()
