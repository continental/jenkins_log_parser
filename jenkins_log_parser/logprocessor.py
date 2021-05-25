"""
The LogProcessor module where the strings come together to produce
a human readable log collection.
"""
import os
from jenkins_log_parser.treewalker import TreeWalker


class LogProcessor:
    """
    The LogProcessor uses all provided classes in this package to
    produce the human readable collection of log files from an jenkins
    log directory.
    """
    def __init__(self, target_path):
        """
        Constructor

        :param target_path: the target path for the produced log files
        """
        self.target_path = target_path
        self.nodes = None
        self.tree = None

    def get_parent_stage(self, current, walker) -> str:
        """
        Retrieves the parent stage of a LogNode

        :param current: the current LogNode
        :param walker: the TreeWalker object used
        :returns: The name of the parent stage or None
        """
        for p in walker.list_parents(current.node_no):
            if p is not None and p.get_step() == "StageStep":
                if p.get_path_text(
                    "./actions/wf.a.LabelAction/displayName"
                ) is not None:
                    p_stage = p.get_path_text(
                        "./actions/wf.a.LabelAction/displayName"
                    )
                    return p_stage
        return None

    def get_parent_parallel(self, current, walker) -> str:
        """
        Retrieves the parent parallel branch name of a LogNode

        :param current: the current LogNode
        :param walker: the TreeWalker object used
        :returns: The name of the parent parallel step or None
        """
        for p in walker.list_parents(current.node_no):
            if p is not None and p.get_step() == "ParallelStep":
                if p.get_path_text(
                    "./actions/\
org.jenkinsci.plugins.workflow.cps\
.steps.ParallelStepExecution_-ParallelLabelAction\
/branchName"
                ) is not None:
                    p_stage = p.get_path_text(
                        "./actions/\
org.jenkinsci.plugins.workflow.cps\
.steps.ParallelStepExecution_-ParallelLabelAction\
/branchName"
                    )
                    return p_stage
        return None

    def process(self, nodes, tree):
        """
        Processes the build log of a Jenkins build

        :param nodes: The nodes dictionary how it is provided by the BuildLog
            class
        :param tree: The tree of nodes also from the BuildLog class
        """
        self.nodes = nodes
        self.tree = tree
        shadow_tree = dict()
        self._split_up(shadow_tree)
        translation = {
            '(': None,
            ')': None,
            "'": None,
            "\"": None,
            ' ': '_',
            "/": "-",
            ",": None,
            "&": "_and_"
        }
        # process tree to find stages and parallel executions
        # stages are a own file, except stages have parallel executions, then
        # the parallel executions are each a own file in a directory named
        # after the stage
        for key, value in shadow_tree.items():
            if value.get("parallel", None) is None:
                print("Got shadow entry %s" % key.translate(
                    str.maketrans(translation)
                ))
                with open(
                    os.path.join(
                        self.target_path,
                        key.translate(str.maketrans(translation))
                    ) + ".log", "w"
                ) as stream:
                    walker = TreeWalker(nodes, tree)
                    current = walker.next()
                    while current is not None:
                        # find first parent stage
                        p_stage = self.get_parent_stage(current, walker)
                        if walker.is_parent_node_of(
                            value.get("lognode").node_no,
                            current.node_no
                        ) and p_stage == key:
                            info = ">>> NodeID: {}, Step: {}\n".format(
                                current.node_no,
                                current.get_step()
                            )
                            stream.write(
                                info
                            )
                            if len(current.indices) > 0:
                                stream.write(current.get_log())
                        current = walker.next()
            else:
                print("Got shadow parallel entry %s" % key)
                stage_dir = key.translate(translation)
                if not os.path.exists(
                    os.path.join(self.target_path, stage_dir)
                ):
                    os.makedirs(os.path.join(self.target_path, stage_dir))
                with open(
                    os.path.join(
                        self.target_path,
                        stage_dir,
                        key.translate(translation)
                    ) + ".log", "w"
                ) as stream:
                    walker = TreeWalker(nodes, tree)
                    current = walker.next()
                    while current is not None:
                        # find first parent stage
                        p_stage = self.get_parent_stage(current, walker)
                        p_parallel = self.get_parent_parallel(current, walker)
                        if walker.is_parent_node_of(
                            value.get("lognode").node_no,
                            current.node_no
                        ) and p_stage == key and p_parallel is None:
                            info = ">>> NodeID: {}, Step: {}\n".format(
                                current.node_no,
                                current.get_step()
                            )
                            stream.write(
                                info
                            )
                            if len(current.indices) > 0:
                                stream.write(current.get_log())
                        current = walker.next()
                for k, v in value.get("parallel").items():
                    with open(
                        os.path.join(
                            self.target_path,
                            stage_dir,
                            k
                        ) + ".log", "w"
                    ) as stream:
                        walker = TreeWalker(nodes, tree)
                        current = walker.next()
                        while current is not None:
                            p_parallel = self.get_parent_parallel(
                                current, walker
                            )
                            if walker.is_parent_node_of(
                                v.node_no,
                                current.node_no
                            ) and p_parallel == k:
                                stream.write(
                                    ">>> NodeID: {}, Step: {}\n".format(
                                        current.node_no,
                                        current.get_step()
                                    )
                                )
                                if len(current.indices) > 0:
                                    stream.write(current.get_log())
                            current = walker.next()

    def _split_up(self, shadow_tree):
        """
        Internal method to split up the tree to a shadow tree containing the
        stages and parallel executions.

        :param shadow_tree: The shadow_tree dictionary used
        """
        walker = TreeWalker(self.nodes, self.tree)
        current = walker.next()
        while current is not None:
            node = current
            step = node.get_step()
            if (
                step == "StageStep" and
                node.get_path_text("./actions/wf.a.LabelAction/displayName")
                    is not None
            ):
                display_name = node.get_path_text(
                    "./actions/wf.a.LabelAction/displayName"
                )
                new = {
                    "lognode": node
                }
                shadow_tree.update({
                    display_name: new
                })
            if (
                step == "ParallelStep" and
                node.get_path_text(
                    "./actions/org.jenkinsci.plugins.workflow.cps.steps.ParallelStepExecution_-ParallelLabelAction/branchName") is not None  # noqa
            ):
                p_stage = self.get_parent_stage(current, walker)
                if shadow_tree.get(p_stage).get("parallel", None) is None:
                    shadow_tree.get(p_stage).update({"parallel": dict()})
                branch_name = node.get_path_text(
                    "./actions/\
org.jenkinsci.plugins.workflow.cps\
.steps.ParallelStepExecution_-ParallelLabelAction\
/branchName"
                )
                shadow_tree.get(p_stage).get("parallel").update({
                    branch_name: node
                })
            current = walker.next()
