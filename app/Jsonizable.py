# -*- coding: UTF-8 -*-
import json
import copy


class Jsonizable(object):
    def to_json_string(self):
        """json序列化"""
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_json(self):
        return copy.copy(self.__dict__)

    def from_json_string(self, jsonstr, cols):
        """判断cols中项是否都在jsonstr序列化之后"""
        self.from_json(json.loads(jsonstr), cols)

    def from_json(self, obj, cols, check=True):
        if check:
            for c in cols:
                if c not in obj:
                    raise Exception("missing %s" % c)
        self.__dict__.update(obj)
