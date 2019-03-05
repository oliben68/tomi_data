from hopla.base.shared.meta_singleton import MetaSingleton
from neo4j import GraphDatabase
from neobolt.exceptions import ServiceUnavailable
from tomi_config import CONFIG

from tomi_data.persistency.operation import Operation, OperationType


class GraphDb(metaclass=MetaSingleton):
    @property
    def driver(self):
        return self._driver

    @property
    def operations(self):
        return self._operations

    def __init__(self):
        init_operation = Operation(OperationType.INIT)
        self._driver = None
        self._operations = {}
        try:
            self._driver = GraphDatabase.driver(
                "{protocol}://{host}:{port}".format(protocol=CONFIG.DB_CONFIG["server"]["protocol"],
                                                    host=CONFIG.DB_CONFIG["server"]["host"],
                                                    port=CONFIG.DB_CONFIG["server"]["port"]),
                auth=(CONFIG.DB_CONFIG["user"]["name"], CONFIG.DB_CONFIG["user"]["password"]))
        except ServiceUnavailable as ex:
            init_operation.data = ex
        self._operations[init_operation.timestamp] = init_operation


NEO_INSTANCE = GraphDb()