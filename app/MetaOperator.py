# -*- coding: UTF-8 -*-
from app.AbstractStorage import AbstractStorage
from app.MetaObject import EntityMeta, PropertyMeta, LinkMeta

'''
table:entity
id
name
desc
parent_id
'''


class MetaOperator:
    """db--> mo_meta
       entity
       link
       property
       entity_property
       link_property
    """

    def __init__(self, storage, accumulator, conf, metaCache):
        if not isinstance(storage, AbstractStorage):
            raise Exception("Wrong Storage Type")
        self.storage = storage
        self.accumulator = accumulator
        self.entity_table = conf.entity_table
        self.link_table = conf.link_table
        self.property_table = conf.property_table
        self.entity_prop_table = conf.entity_prop_table
        self.link_prop_table = conf.link_prop_table
        self.meta_cache = metaCache

    def get_all_entities(self):
        """获取某个table所有entity数据"""
        return self.__gen_entity_objs(self.storage.get_all(self.entity_table))

    def get_entity_by_name(self, name):
        """通过name获取对应entity数据"""
        return self.__gen_entity_objs(self.storage.get_by_query(self.entity_table, {"name": name}))

    def get_entity(self, id):
        """获取某一条entity数据"""
        return self.__gen_obj(EntityMeta, self.storage.get_by_id(self.entity_table, int(id)))

    def delete_entity(self, id):
        """删除某一条"entity数据"""
        self.storage.delete(self.entity_table, int(id))
        return id

    def __gen_obj(self, ObjClass, data):
        """
        data转化为json返回
        :param ObjClass:  EntityMeta
        :param data: 每一行的数据
        :return: json
        """
        if data is None:
            return {}
        d = ObjClass()
        d.from_json(data, False)
        return d.to_json()

    def __gen_entity_objs(self, data):
        """
        获取实体数据列表
        :param data:obj, 所有collection的列表
        :return: json, 所有转化为json后的列表
        """
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(EntityMeta, i))
        return res

    def put_entity(self, name, eng_name, desc, eng_desc, pid):
        """
        对于entity
        数据库中   put
        内存中    upsert_entity
        """
        d = EntityMeta(self.accumulator.GetId(), name, eng_name, desc, eng_desc, pid)
        self.storage.put(self.entity_table, d.to_json())
        self.meta_cache.upsert_entity(d)
        return d.id

    def put_entity_prop(self,
                        name,
                        eng_name,
                        desc,
                        eng_desc,
                        entity_id,
                        type,
                        number_of_value,
                        enum_value,
                        eng_enum_value):
        """
        对于 entity_prop
        数据库中   put
        内存中    upsert_entity_prop

        """
        d = PropertyMeta(
            self.accumulator.GetId(), name, eng_name, desc, eng_desc, entity_id, type, number_of_value, enum_value,
            eng_enum_value)
        self.storage.put(self.entity_prop_table, d.to_json())
        self.meta_cache.upsert_entity_prop(d)
        return d.id

    def delete_entity_prop(self, id):
        self.storage.delete(self.entity_prop_table, int(id))
        return id

    def get_entity_prop(self, entity_id):
        return self.__gen_entity_prop_objs(
            self.storage.get_by_query(self.entity_prop_table, {"elid": entity_id}))

    def get_all_entity_props(self):
        return self.__gen_entity_prop_objs(
            self.storage.get_all(self.entity_prop_table))

    def get_property_by_name(self, property_name):
        res = self.storage.get_by_query(self.property_table, {{"$text": {"$search": property_name}}})
        return self.__gen_prop_objs(res)

    def get_all_properties(self):
        return self.__gen_prop_objs(self.storage.get_all(self.property_table))

    def put_property(self, name, desc, elid, type, enum_value):
        """
        对于 property
        数据库中   put
        内存中    upsert_property
        """
        d = PropertyMeta(self.accumulator.GetId(), name, desc, elid, type, enum_value)
        self.storage.put(self.property_table, d.to_json())
        self.meta_cache.upsert_property(d)
        return d.id

    def __gen_prop_objs(self, data):
        """获取属性"""
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(PropertyMeta, i))
        return res

    def __gen_entity_prop_objs(self, data):
        """通过实体获取属性"""
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(PropertyMeta, i))
        return res

    def get_all_links(self):
        return self.__gen_link_objs(
            self.storage.get_all(self.link_table))

    def get_link_by_name(self, name):
        res = self.storage.get_by_query(self.property_table, {{"$text": {"$search": name}}})
        return self.__gen_link_objs(res)

    def get_link(self, link_id):
        return self.__gen_obj(
            LinkMeta,
            self.storage.get_by_id(self.link_table, link_id))

    def put_link(self, name, eng_name, desc, eng_desc, pid, src_entity, dest_entity):
        """
        对于 link
        数据库中   put
        内存中    upsert_link
        """
        d = LinkMeta(self.accumulator.GetId(), name, eng_name, desc, eng_desc, pid, src_entity, dest_entity)
        self.storage.put(self.link_table, d.to_json())
        self.meta_cache.upsert_link(d)
        return d.id

    def delete_link(self, id):
        self.storage.delete(self.link_table, int(id))
        return id

    def put_link_prop(
            self, name, eng_name, desc, eng_desc, link_id, type, number_of_value, enum_value, eng_enum_value):
        """
        对于 link_prop
        数据库中   put
        内存中    upsert_entity_prop
        """
        d = PropertyMeta(
            self.accumulator.GetId(), name, eng_name, desc, eng_desc, link_id, type, number_of_value, enum_value,
            eng_enum_value)
        self.storage.put(self.link_prop_table, d.to_json())
        self.meta_cache.upsert_entity_prop(d)
        return d.id

    def delete_link_prop(self, id):
        self.storage.delete(self.link_prop_table, int(id))
        return id

    def get_link_prop(self, link_id):
        """get_one"""
        return self.__gen_entity_prop_objs(
            self.storage.get_by_query(self.link_prop_table, {"elid": link_id}))

    def get_all_link_props(self):
        """get_all"""
        return self.__gen_entity_prop_objs(
            self.storage.get_all(self.link_prop_table))

    def __gen_link_objs(self, data):
        """获取关系属性"""
        res = []
        if data is None:
            return res
        for i in data:
            res.append(self.__gen_obj(LinkMeta, i))
        return res
