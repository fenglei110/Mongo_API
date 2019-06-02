# coding=utf-8
class Accumulator:
    """累加器"""
    def __init__(self, storage):
        self.storage = storage

    def GetId(self):
        """专门建一张表，只存储当前id用于记录递增"""
        return self.storage.gen_id('id_gener')