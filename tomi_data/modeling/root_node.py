from uuid import uuid4

from tomi_data.modeling.document_node import DocumentNode


class RootNode(DocumentNode):
    ROOT_NODE_NAME = "root"

    def __init__(self, key, name):
        super().__init__(id="{root}::{id}".format(root=RootNode.ROOT_NODE_NAME, id=uuid4()), key=key, name=name)
        super().freeze()

    # disabling freeze and unfreeze methods
    def freeze(self):
        pass

    unfreeze = freeze
