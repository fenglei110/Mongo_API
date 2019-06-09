# coding=utf-8
from app.Jsonizable import Jsonizable
from app.Timestamp import Timestamp


class EntityData(Jsonizable):
    """
    mo_data---> entity
    """
    cols = ["id", "name", "eng_name", "typeid", "timestamp"]

    def __init__(self,
                 id=None,
                 name=None,
                 eng_name=None,
                 typeid=None,
                 timestamp=Timestamp.sec_now()):
        self.id = id
        self.name = name
        self.typeid = typeid
        self.timestamp = timestamp
        self.eng_name = eng_name

    def from_json(self, obj, check=True):
        """
        把obj update到self.__dict__, 而且cols每一项都在obj中
        """
        super(EntityData, self).from_json(obj, EntityData.cols, check)

    def from_json_string(self, jsonstr):
        """
        把jsonstr序列化后 update到self.__dict__, 而且cols每一项都在obj中
        """
        super(EntityData, self).from_json_string(jsonstr, EntityData.cols)


class PropertyData(Jsonizable):
    """
    mo_data---> property
    """
    cols = ["id", "elid", "typeid", "value", "eng_value", "timestamp"]

    def __init__(self,
                 id=None,
                 elid=None,
                 typeid=None,
                 value=None,
                 eltype=None,
                 eng_value=None,
                 timestamp=Timestamp.sec_now()):
        self.id = id
        self.elid = elid
        self.typeid = typeid
        self.value = value
        self.eltype = eltype
        self.timestamp = timestamp
        self.eng_value = eng_value

    def from_json(self, obj, check=True):
        super(PropertyData, self).from_json(obj, PropertyData.cols, check)

    def from_json_string(self, jsonstr):
        super(PropertyData, self).from_json_string(jsonstr, PropertyData.cols)


class LinkData(Jsonizable):
    """
    mo_data---> link
    """
    cols = ["id", "src", "dest", "typeid", "timestamp"]

    def __init__(self,
                 id=None,
                 src=None,
                 dest=None,
                 typeid=None,
                 timestamp=Timestamp.sec_now()):
        self.id = id
        self.src = src
        self.dest = dest
        self.typeid = typeid
        self.timestamp = timestamp

    def from_json(self, obj, check=True):
        super(LinkData, self).from_json(obj, LinkData.cols, check)

    def from_json_string(self, jsonstr):
        super(LinkData, self).from_json_string(jsonstr, LinkData.cols)
