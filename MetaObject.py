# -*- coding: UTF-8 -*-
# 针对mo_meta各个表的处理
from Jsonizable import Jsonizable


class MetaStatus:
    OK = 0
    DISCARD = 1


class EntityMeta(Jsonizable):
    """db----> mo_meta
      table---> entity
    """
    cols = ["id", "name", "eng_name", "desc", "eng_desc", "pid", "status"]

    def __init__(self,
                 id=None,
                 name=None,
                 eng_name=None,
                 desc=None,
                 eng_desc=None,
                 pid=None,
                 status=MetaStatus.OK):
        self.id = id
        self.name = name
        self.desc = desc
        self.pid = pid
        self.eng_name = eng_name
        self.eng_desc = eng_desc
        self.status = status

    def from_json(self, obj, check=True):
        """校验obj中字段的正确性"""
        super(EntityMeta, self).from_json(obj, EntityMeta.cols, check)

    def from_json_string(self, jsonstr):
        super(EntityMeta, self).from_json_string(jsonstr, EntityMeta.cols)


class PropertyTypes:
    """对 proerty type 的验证"""
    STRING = "string"
    NUMBER = "number"
    ENUM_NUMBER = "enum_number"
    ENUM_STRING = "enum_string"
    LIST_NUMBER = "list_number"
    LIST_STRING = "list_string"
    DATE = "date"
    types = [STRING, NUMBER, ENUM_NUMBER, ENUM_STRING, LIST_NUMBER, LIST_STRING, DATE]

    def __init__(self):
        pass

    @staticmethod
    def string(type):
        return type == PropertyTypes.STRING or type == PropertyTypes.ENUM_STRING

    @staticmethod
    def number(type):
        return type == PropertyTypes.NUMBER or type == PropertyTypes.ENUM_NUMBER

    @staticmethod
    def validate(type):
        return type in PropertyTypes.types

    @staticmethod
    def enum(type):
        return type == PropertyTypes.ENUM_NUMBER or type == PropertyTypes.ENUM_STRING

    @staticmethod
    def list(type):
        return type == PropertyTypes.LIST_NUMBER or type == PropertyTypes.LIST_STRING

    @staticmethod
    def date(type):
        return type == PropertyTypes.DATE


class PropertyValueNumber:
    SINGLE = 0
    MULTIPLE = 1

    def __init__(self):
        pass

    @staticmethod
    def single(t):
        """
        :param t:  int
        :return:   bool
        """
        return t == PropertyValueNumber.SINGLE

    @staticmethod
    def multiple(t):
        """
        :param t:  int
        :return:  bool
        """
        return t == PropertyValueNumber.MULTIPLE


class PropertyMeta(Jsonizable):
    """db---> mo_meta
       table----> link_property / entity_property
    """
    cols = ["id", "name", "eng_name", "desc", "eng_desc", "elid", "type", "number_of_value", "enum_value",
            "eng_enum_value", "status"]

    def __init__(self,
                 id=None,
                 name=None,
                 eng_name=None,
                 desc=None,
                 eng_desc=None,
                 elid=None,
                 type=None,
                 number_of_value=PropertyValueNumber.SINGLE,
                 enum_value=None,
                 eng_enum_value=None,
                 status=MetaStatus.OK):
        self.id = id
        self.name = name
        self.desc = desc
        self.elid = elid
        self.type = type
        self.enum_value = enum_value
        self.eng_name = eng_name
        self.eng_desc = eng_desc
        self.number_of_value = number_of_value
        self.eng_enum_value = eng_enum_value
        self.status = status

    def from_json(self, obj, check=True):
        super(PropertyMeta, self).from_json(obj, PropertyMeta.cols, check)

    def from_json_string(self, jsonstr):
        super(PropertyMeta, self).from_json_string(jsonstr, PropertyMeta.cols)


class LinkMeta(Jsonizable):
    """
    db----> mo_meta
    table----> link
    """
    cols = ["id", "name", "eng_name", "desc", "eng_desc", "pid", "src_entity", "dest_entity"]

    def __init__(self,
                 id=None,
                 name=None,
                 eng_name=None,
                 desc=None,
                 eng_desc=None,
                 pid=None,
                 src_entity=None,
                 dest_entity=None,
                 status=MetaStatus.OK):
        self.id = id
        self.name = name
        self.desc = desc
        self.pid = pid
        self.eng_name = eng_name
        self.eng_desc = eng_desc
        self.src_entity = src_entity
        self.dest_entity = dest_entity
        self.status = status

    def from_json(self, obj, check=True):
        super(LinkMeta, self).from_json(obj, LinkMeta.cols, check)

    def from_json_string(self, jsonstr):
        super(LinkMeta, self).from_json_string(jsonstr, LinkMeta.cols)
