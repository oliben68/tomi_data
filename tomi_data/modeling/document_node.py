from tomi_graph.entity_class_generator import EntityClassGenerator
from tomi_graph.nodes.node_class import NodeBaseClass
from tomi_graph.version_aware_entity import VersionAwareEntity


DocumentNode = EntityClassGenerator(NodeBaseClass, VersionAwareEntity).create("Document")
