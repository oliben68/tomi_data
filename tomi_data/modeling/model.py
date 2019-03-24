from tomi_graph.graphs.graph import Graph

from tomi_data.modeling.root_node import RootNode


class Model(Graph):
    @property
    def root(self):
        return self._root

    def __init__(self):
        super().__init__(namespace_root=Graph.NAMESPACE_DELIMITER)
        root_node = RootNode()
        self.add_node(root_node)
        self._root = root_node
        self.protect(root_node.id)

    def protect(self, key):
        if key in self.nodes.keys():
            self.nodes.protect(key)

    def lift_protection(self, key):
        if not key.startswith("{root}::".format(root=RootNode.ROOT_NODE_NAME)):
            self.nodes.lift_protection(key)


