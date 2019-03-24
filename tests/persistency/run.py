from tomi_graph.nodes.node_class import NodeBaseClass
from tomi_graph.entity_class_generator import EntityClassGenerator
from tomi_graph.version_aware_entity import VersionAwareEntity
from tomi_graph.indexes_support import IndexesSupport

from tomi_data.persistency.generators.cypher.graph_commands import GraphCommands

NodeTest = EntityClassGenerator(NodeBaseClass, VersionAwareEntity, IndexesSupport).create("NodeTest")

ids = ["A", "B", "C", "D", "E", "ROOT"]

d_a = NodeTest(ids[0], id=ids[0])
d_b = NodeTest(ids[1], id=ids[1])
d_c = NodeTest(ids[2], id=ids[2])
d_d = NodeTest(d_a, d_b, d_c, id=ids[3])
d_e = NodeTest([{"D_d": d_d}], id=ids[4])
root = NodeTest(d_e, id="Root")
g = root.graph


from tomi_data.persistency.generators.cypher.graph_commands import GraphCommands
cms = GraphCommands(g).save_all()