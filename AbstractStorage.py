# -*- coding: UTF-8 -*-


class AbstractStorage:
    """基类，用于存取"""

    def get_by_id(self, id, *args):
        pass

    def get_by_query(self, kvs, *args):
        pass

    def put(self, kvs, *args):
        pass

    def get_multi(self, key, *args):
        pass

    def update(self, id, value, *args):
        pass

    def delete(self, key, *args):
        pass

    def get_all(self, key, *args):
        pass
