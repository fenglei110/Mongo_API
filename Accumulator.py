# coding=utf-8
class Accumulator:
    """累加器"""
    def __init__(self, storage):
        self.storage = storage

    def GetId(self):
        """返回id"""
        return self.storage.gen_id('id_gener')