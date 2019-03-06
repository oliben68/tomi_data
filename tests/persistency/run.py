from tomi_base.base.graphs.nodes.node import Node

from tomi_base.persistency.dal.neo4j import CypherOperations
from tomi_base.persistency.generators import NodeCommands

n1 = Node({"test": {"value": "ABC"}})
CypherOperations.create_node(n1)
nsg1 = NodeCommands(n1)

n2 = Node({"test": {"value": "BCD"}})
CypherOperations.create_node(n2)
nsg2 = NodeCommands(n2)

r1 = (n1 < n2)(rel_type="buddies_ole_boys",
               data={"how": {"we": "test"}, "the depth": "of", "our souls": {"is": "a mystery"}})
# matches = "{m1}, {m2}".format(
#     m1=nsg1.self_generate_match(excluded=["__create_date", "__update_date"], variable="n1"),
#     m2=nsg2.self_generate_match(excluded=["__create_date", "__update_date"], variable="n1"))
# print(RelationshipCommands(r1).self_generate_create(variable="r1"))

# result = CypherOperations.create_nodes_relationship(n1, n2, rel_type="BUDDINSKY", variable='r')
result = CypherOperations.delete_all()  # create_relationship(r1, variable='r')
result
