# -*- coding: UTF-8 -*-
from DataObject import EntityData, LinkData, PropertyData
from StatusCode import StatusCode


class DataOperator(object):
    """
    db-----> mo_data
    对 entity  link  property 数据进行增删改查
    """
    def __init__(self, storage, accumulator, metaCache, tableConf):
        self.storage = storage
        self.accumulator = accumulator
        self.entity_table = tableConf.entity_table
        self.link_table = tableConf.link_table
        self.property_table = tableConf.property_table
        self.metaCache = metaCache

    """
    entity:
    id(uniq)
    name(index)
    desc(index)
    type: entity_meta_id
    timestamp
    
    link:
    id(uniq)
    src: entityid
    dest: entityid
    type: link_meta_id
    timestamp
    
    property:
    id(uniq)
    elid
    property_type
    value
    """

    def get_entity_by_id(self, id):
        """
        entity  get_entity_by_id
        """
        return self.__gen_obj(EntityData, self.storage.get_by_id(self.entity_table, id))

    def get_entity_by_name(self, name):
        """
        entity  get_entity_by_name
        """
        return self.__gen_entity_objs(
            self.storage.get_by_query(self.entity_table, {"name": "/%s/i" % name}))

    def put_entity(self, name, eng_name, typeid):
        """
        entity 获取累加器id，然后put
        """
        data = EntityData(self.accumulator.GetId(), name, eng_name, typeid)
        self.storage.put(self.entity_table, data.to_json())
        return data.id

    def update_entity(self, entity_id, name, eng_name):
        """
        entity update by name
        """
        if name is not None:
            res = self.storage.update(
                self.entity_table, entity_id, {"name": name})
            if res is None:
                return StatusCode.NotExists, None

        if eng_name is not None:
            res = self.storage.update(
                self.entity_table, entity_id, {"eng_name": eng_name})
            if res is None:
                return StatusCode.NotExists, None

        return StatusCode.OK, entity_id

    def delete_entity(self, entity_id):
        """
        entity delete by id
        """
        res = self.storage.delete_by_id(self.entity_table, entity_id)
        res = self.storage.delete_by_query(self.property_table, {"elid": entity_id})
        return entity_id

    def __gen_obj(self, ObjClass, data):
        """
        data转化为json返回
        :param ObjClass:  EntityMeta / LinkMeta
        :param data:      collection
        :return:          json
        """
        if data is None:
            return {}
        d = ObjClass()
        d.from_json(data, False)
        return d.to_json()

    def __gen_entity_objs(self, data):
        """
        :param data:  obj, 多个collection的列表
        :return:     list, 所有转化为json后的列表
        """
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(EntityData, i))
        return res

    def get_link_by_id(self, id):
        """
        link get by id
        """
        return self.__gen_obj(
            LinkData,
            self.storage.get_by_id(self.entity_table, id))

    def get_link_by_entity(self, entity_id):
        """
        link get by entity_id
        """
        return self.__gen_link_objs(
            self.storage.get_by_query(self.link_table, {"or": [{"src": entity_id}, {"dest": entity_id}]}))

    def put_link(self, src, dest, typeid):
        """
        link 获取累加器id  put
        """
        data = LinkData(self.accumulator.GetId(), src, dest, typeid)
        self.storage.put(self.link_table, data.to_json())
        return data.id

    def delete_link(self, link_id):
        """
        link delete by id
        """
        res = self.storage.delete_by_id(self.link_table, link_id)
        res = self.storage.delete_by_query(
            self.property_table, {"elid": link_id})
        return link_id

    def __gen_link_objs(self, data):
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(LinkData, i))
        return res

    def get_property(self, elid):
        """
        通过entity_id 获取所有property
        封装成  { 102:['{}', '{}'], 103:[ ] }
        """
        query = {"elid": elid}
        obj_res = self.__gen_prop_objs(
            self.storage.get_by_query(self.property_table, query))

        res = {}
        for item in obj_res:
            t = item.typeid
            if t in res:
                res[t].append(item.to_json())
            else:
                res[t] = [item.to_json()]

        return res

    def put_property(self, elid, property_type, value, eng_value, is_entity):
        """ property put """
        eltype = 0
        if not is_entity:
            eltype = 1
        data = PropertyData(self.accumulator.GetId(),
                            elid,
                            property_type,
                            value,
                            eltype,
                            eng_value)

        self.storage.put(self.property_table, data.to_json())
        return data.id

    def update_property(self, prop_id, value=None, eng_value=None):
        """ property update_one by prop_id"""
        res = None
        if value is not None:
            res = self.storage.update(self.property_table, prop_id, {"value": value})
            if res is None:
                return StatusCode.NotExists, None

        if eng_value is not None:
            res = self.storage.update(self.property_table, prop_id, {"eng_value": eng_value})
            if res is None:
                return StatusCode.NotExists, None

        p = PropertyData()
        p.from_json(res)
        return StatusCode.OK, p

    def get_property_by_id(self, prop_id):
        """property get by id"""
        res = self.storage.get_by_id(self.property_table, prop_id)
        if res is None:
            return None

        d = PropertyData()
        d.from_json(res)
        return d

    def __gen_prop_objs(self, data):
        res = []
        if data is None:
            return res
        for i in data:
            d = PropertyData()
            d.from_json(i)
            res.append(d)
        return res

    def delete_property(self, prop_id):
        """delete by id"""
        res = self.storage.delete_by_id(self.property_table, prop_id)

        return prop_id
