"""
Module for handling a Jenkins build log directory or zip file
"""
import os
import glob
import tempfile
import zipfile
from jenkins_log_parser.lognode import LogNode


class BuildLog():
    """
    The BuildLog class is the entrypoint for collecting all necessary
    data of a jenkins build log directory.
    """
    def __init__(self, log_location):
        """
        Constructor.

        :param log_location: The directory or zip archive of the log data
        """
        self.log_dir = None
        self.tempdir = None
        if os.path.isdir(log_location):
            self.log_dir = log_location
        else:
            if log_location.endswith(".zip"):
                self.tempdir = tempfile.TemporaryDirectory()
                self.log_dir = self.tempdir.name
                archive = zipfile.ZipFile(log_location)
                archive.extractall(self.log_dir)

        self.log_file = None
        self.log_index = None
        os.chdir(self.log_dir)
        self.log_index = glob.glob("**/log-index", recursive=True)[0]
        self.log_file = glob.glob("**/log", recursive=True)[0]
        self.nodes = dict()

    def __del__(self):
        if self.tempdir is not None:
            self.tempdir.cleanup()

    def collect_nodes(self):
        """
        Collects all workflow nodes and saves them in an internal dict
        also returning it for further use.

        :returns: A dictionary of the log id mapped to an LogNode object
        """
        files = glob.glob("**/workflow/*.xml", recursive=True)
        for f in files:
            fname = f.split(os.path.sep)[-1]
            nodeid = fname.split(".")[0]
            if nodeid.isdecimal():
                # nodeid content which is not decimal is skipped!
                self.nodes.update({
                    int(nodeid): LogNode(int(nodeid))
                })
            else:
                raise ValueError(
                    "All nodes have to be in decimal, here a node with the\
 name '%s' exists." % nodeid)
        return self.nodes

    def collect_nodes_logs(self):
        """
        Parses the provided log-index and matches the found log byte positions
        to the LogNode objects in the internal dictionary.

        This call is required for being able to produce the output.
        """
        if self.nodes is None:
            self.collect_nodes()
        index_data = []
        with open(self.log_index, "r") as stream:
            index_data = stream.readlines()
        i = 0
        step = 2
        while i < len(index_data):
            try:
                log_start = index_data[i].split()
                log_end = list()
                if i+1 < len(index_data):
                    log_end = index_data[i+1].split()
                else:
                    break
                if len(log_end) > 1:
                    step = 1
                else:
                    step = 2
                self.nodes.get(
                    int(log_start[1])
                ).add_index(
                    int(log_start[0]),
                    int(log_end[0])
                )
                self.nodes.get(
                    int(log_start[1])
                ).set_log_file(self.log_file)
            except Exception as e:
                print("%s: %s" % (i, index_data[i]))
                raise e

            i = i+step

    def create_tree(self):
        """
        Creates a tree like structure where the parent-child relationships of
        the LogNodes are stored. This tree structure can then be traversed
        with the TreeWalker class.

        :returns: A dictionary containing a tree like structure for the use
            with TreeWalker
        """
        tree = {}
        for nodeid in sorted(self.nodes.keys()):
            parent_id = self.nodes[nodeid].parent_id
            if parent_id not in tree:
                tree.update({parent_id: [nodeid]})
            else:
                tree.get(parent_id).append(nodeid)
            tree.update({nodeid: []})
        return tree
