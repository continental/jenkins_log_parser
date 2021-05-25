"""
The LogNode module representing a node in the workflow process of jenkins
"""
import xml.etree.ElementTree as ET
import glob


class LogNode:
    """
    The LogNode class provides information directly out of the xml
    structure
    """
    def __init__(self, node_no: int, start: int = None, end: int = None):
        """
        Constructor

        :param node_no: node number
        :param start: the start byte of this node number in the log (optional)
        :param end: the end byte of this node number in the log (optional)
        """
        self.node_no = node_no
        files = glob.glob(
            "**/{}.xml".format(self.node_no),
            recursive=True
        )
        self.node_file = files[0]
        self.root = ET.parse(self.node_file).getroot()
        self.parent_id = self.get_parent_id()
        self.log_file = None
        self.indices = list()
        if start is not None and end is not None:
            self.indices.append({
                "start": start,
                "end": end
            })

    def __repr__(self) -> str:
        """
        Some string representation

        :returns: Just the node number as string
        """
        return "{}".format(self.node_no)

    def set_log_file(self, log_file):
        """
        Method to set the log file needed for extracting the log snipped this
        workflow node represents

        :param log_file: the log file
        """
        self.log_file = log_file

    def get_log(self) -> str:
        """
        Opens the log file and extracts the defined log snippet.

        :returns: The log snippet as string or None if no start or end byte
            is set
        """
        if len(self.indices) == 0:
            return None
        log = ""
        with open(self.log_file, "rb") as stream:
            for index in self.indices:
                stream.seek(index.get("start"))
                log += stream.read(
                    index.get("end") - index.get("start")
                ).decode()
        return log

    def get_log_part(self, start: int, end: int):
        """
        Convenience method to retrieve any snippet from the log file

        :param start: the start byte number
        :param end: the end byte number
        :returns: the log snippet as string
        """
        log = None
        with open(self.log_file, "rb") as stream:
            stream.seek(start)
            log = stream.read(end-start).decode()
        return log

    def add_index(self, start: int, end: int):
        """
        Set the internal start and end byte position

        :param start: the start byte number
        :param end: the end byte number
        """
        self.indices.append({
            "start": start,
            "end": end
        })

    def get_node_class(self) -> str:
        """
        Retrieves the node's class attribute

        :returns: the node's class attribute as string
        """
        node = self.root.find("node")
        return node.get("class")

    def get_node_descriptorId(self) -> str:
        """
        Retrieves the descriptorId of the node (usually the pipeline Step type)

        :returns: the descriptorId as string
        """
        node = self.root.find("node")
        if node is not None:
            desc = node.find("descriptorId")
            if desc is not None:
                return desc.text
        return None

    def get_step(self) -> str:
        """
        Cuts all the unnecessary class tree information from the step type

        :returns: the step class name without package information
        """
        descriptor = self.get_node_descriptorId()
        if descriptor is not None:
            return descriptor.split(".")[-1]
        return None

    def get_path_text(self, path) -> str:
        """
        Returns the content of a xml path element

        :param path: the path to the xml element
        :returns: the content of the xml element as string
        """
        target = self.root.find(path)
        if target is not None:
            return target.text
        return None

    def get_parent_id(self) -> int:
        """
        Method to read out the parent id of a node

        :returns: The parent id as integer
        """
        node = self.root.find("node")
        if node is not None:
            parentIds = node.find("parentIds")
            if parentIds is not None:
                parentId = parentIds.find("string")
                if parentId is not None:
                    return int(parentId.text)
        return None
