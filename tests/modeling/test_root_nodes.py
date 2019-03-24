from tomi_data.modeling.root_node import RootNode


def test_root_node():
    name = "ROOT_NODE"
    key = "1234567890"
    root = RootNode(name=name, key=key)

    assert root.name is not None
    assert root.key is not None
    assert RootNode.ROOT_NODE_NAME in root.id
    assert root.name == name
    assert root.key == key

    root_dict = root.toDict()
    assert root_dict["__type"] == RootNode.__name__
