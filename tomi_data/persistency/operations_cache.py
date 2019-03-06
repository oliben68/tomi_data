import ujson
from collections.abc import MutableMapping

from tomi_base.shared.logging.facade import Slf4p
from tomi_data.persistency.operation import Operation


@Slf4p()
class OperationsCache(MutableMapping):
    def __init__(self, max_count=None, *args, **kwargs):
        if max_count is None:
            self._max_count = 1000
        else:
            try:
                self._max_count = int(max_count)
            except:
                self._max_count = 1000
        self.__dict = {}
        self.__dict.update(*args, **kwargs)

    def append(self, value):
        if type(value) != Operation:
            raise TypeError("The value needs to be of type '{t}'".format(t=Operation.__name__))

        self.__dict[value.timestamp] = value

        self.log.info(value)

        if len(self) > self._max_count:
            del self.__dict[sorted(self.__dict.keys())[0]]

    def __setitem__(self, _, __):
        pass

    def __getitem__(self, key):
        return self.__dict[key]

    def __delitem__(self, key):
        del self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __str__(self):
        return ujson.dumps(self.__dict)
