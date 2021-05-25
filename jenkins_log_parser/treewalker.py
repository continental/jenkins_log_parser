"""
The TreeWalker module
"""
from jenkins_log_parser.lognode import LogNode


class TreeWalker:
    """
    The TreeWalker class is meant for traversing the tree produced by
    the class BuildLog in an orderly manner.
    """
    def __init__(self, nodes, tree):
        """
        Constructor

        :param nodes: The nodes how the class BuildLog is providing them
        :param tree: The tree structure BuildLog is providing
        """
        self.nodes = nodes
        self.tree = tree.copy()
        self.current = None
        self.done = []

    def next(self) -> LogNode:
        """
        Proceed to the next LogNode and return it like the tree structure
        dictates
        """
        if self.current is not None:
            self.done.append(self.current)
        else:
            self.current = self.tree.get(self.current)[0]
            del self.tree[None]
            return self.nodes.get(self.current)
        for i in self.tree.get(self.current):
            if i not in self.done:
                self.current = i
                return self.nodes.get(self.current)
        for i in sorted(self.tree.keys()):
            if i not in self.done:
                self.current = i
                return self.nodes.get(self.current)
        return None

    def is_parent_node_of(self, probable_parent, node_no) -> bool:
        """
        Boolean method to check if a node is a parent of another node

        :param probable_parent: the node number of the probable parent
        :param node_no: the node number to check
        :returns: True or False
        """
        current = node_no
        while current is not None:
            current = self.nodes.get(current).parent_id
            if current == probable_parent:
                return True
        return False

    def depth(self, node_no) -> int:
        """
        Calculate the depth of a node inside the tree

        :param node_no: the node to calculate
        :returns: the depth in integer
        """
        current = node_no
        i = 0
        while current is not None:
            current = self.nodes.get(current).parent_id
            i += 1
        return i

    def list_parents(self, node_no) -> list:
        """
        Creates a list of parents up to the root node

        :param node_no: the node number which's list should be created
        :returns: a list of nodes starting with the first parent and ending
            with the root node
        """
        current = node_no
        parents = []
        while current is not None:
            current = self.nodes.get(current).parent_id
            parents.append(self.nodes.get(current))
        return parents

    def start_from(self, node_no: int):
        """
        A method to set the start node in an traversal (Deprecated and unused)

        :param node_no: the node number to start from
        """
        self.current = node_no
