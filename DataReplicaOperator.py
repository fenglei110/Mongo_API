# -*- coding: UTF-8 -*-
from DataOperator import DataOperator
from DataObject import EntityData, LinkData, PropertyData
from MetaObject import PropertyValueNumber
from StatusCode import StatusCode


class DataReplicaOperator(DataOperator):
    """
    对mo_data中  entity  link  property 进行增删改查
    """
    def __init__(self, storage, req_storage, accumulator, metaCache, tableConf, repTableConf):
        self.req_storage = req_storage
        self.metaCache = metaCache
        self.rep_entity_table = repTableConf.entity_table
        self.rep_link_table = repTableConf.link_table
        super(DataReplicaOperator, self).__init__(storage, accumulator, metaCache, tableConf)

    def get_all_entity(self, start, size, typeid):
        """entity 查"""
        return self.req_storage.get_by_query_limit(self.rep_entity_table, {"id": {"$gte": start}, "typeid": typeid}, size)

    def put_entity(self, name, eng_name, typeid):
        """
        entity 增
        获取put之后返回的id
        """
        id = super(DataReplicaOperator, self).put_entity(name, eng_name, typeid)
        data = EntityData(id, name, eng_name, typeid)
        self.req_storage.put(self.rep_entity_table, data.to_json())
        return id

    def update_entity(self, entity_id, name, eng_name):
        """"
        entity 改
        """
        code, eid = \
            super(DataReplicaOperator, self).update_entity(entity_id, name, eng_name)

        if code != StatusCode.OK:
            return code, eid

        if name is not None:
            res = self.req_storage.update(
                self.rep_entity_table, entity_id, {"name": name})
            if res is None:
                return StatusCode.NotExists, None

        if eng_name is not None:
            res = self.req_storage.update(
                self.rep_entity_table, entity_id, {"eng_name": eng_name})
            if res is None:
                return StatusCode.NotExists, None

        return code, eid

    def delete_entity(self, entity_id):
        """"entity 删"""
        res = super(DataReplicaOperator, self).delete_entity(entity_id)
        res = self.req_storage.delete_by_id(self.rep_entity_table, entity_id)
        return StatusCode.OK, entity_id

    def get_all_link(self, start, size, typeid):
        """link 查"""
        return self.req_storage.get_by_query_limit(self.rep_link_table, {"id": {"$gte": start}, "typeid": typeid}, size)

    def put_link(self, src, dest, typeid):
        """link 增"""
        id = super(DataReplicaOperator, self).put_link(src, dest, typeid)
        data = LinkData(id, src , dest, typeid)
        self.req_storage.put(self.rep_link_table, data.to_json())
        return id

    def delete_link(self, link_id):
        """link 删"""
        res = super(DataReplicaOperator, self).delete_link(link_id)
        res = self.req_storage.delete_by_id(self.rep_link_table, link_id)

        return StatusCode.OK, link_id

    def put_property(self, elid, property_type, value, eng_value, is_entity):
        """property 增"""
        prop_id = super(DataReplicaOperator, self).put_property(elid, property_type, value, eng_value, is_entity)
        table_name = self.rep_entity_table
        p = None
        if not is_entity:
            table_name = self.rep_link_table

        p = self.metaCache.get_property(property_type)
        if p is None:
            return StatusCode.NotExists, None

        if PropertyValueNumber.single(p.number_of_value):
            res = \
                self.req_storage.update(table_name, elid, {"%s" % property_type: {"c": value, "e": eng_value, "id": prop_id}})
        else:
            res = \
                self.req_storage.update_push(table_name, elid, {"%s" % property_type: {"c": value, "e": eng_value, "id": prop_id}})
        if res is None:
            return StatusCode.NotExists, None

        return StatusCode.OK, prop_id

    def update_property(self, prop_id, value=None, eng_value=None):
        """property 改"""
        code, prop = super(DataReplicaOperator, self).update_property(prop_id, value, eng_value)
        if code != StatusCode.OK:
            return code, None

        table_name = self.rep_entity_table
        if prop.eltype == 1:
            table_name = self.rep_link_table

        p = self.metaCache.get_property(prop.typeid)
        if p is None:
            return StatusCode.OtherError, None

        if PropertyValueNumber.single(p.number_of_value):
            if value is not None:
                self.req_storage.update(table_name, prop.elid, {"%s.c" % prop.typeid: value})

            if eng_value is not None:
                self.req_storage.update(table_name, prop.elid, {"%s.e" % prop.typeid: eng_value})
        else:
            if value is not None:
                self.req_storage.update_mutil_key(
                    table_name,
                    {'id': prop.elid, '%s.id'% prop.typeid: prop_id},
                    {"%s.$.c"% prop.typeid: value})

            if eng_value is not None:
                self.req_storage.update_mutil_key(
                    table_name,
                    {'id': prop.elid, '%s.id'% prop.typeid: prop_id},
                    {"%s.$.e"% prop.typeid: eng_value})

        return StatusCode.OK, prop_id

    def delete_property(self, prop_id):
        """property 删"""
        p = super(DataReplicaOperator, self).get_property_by_id(prop_id)
        if p is None:
            return StatusCode.NotExists, prop_id

        res = super(DataReplicaOperator, self).delete_property(prop_id)
        table_name = self.rep_entity_table
        if p.eltype == 1:
            table_name = self.rep_link_table

        query = {'%s'% p.typeid: {'id': p.id}}
        res = self.req_storage.update_pull(table_name, p.elid, query)
        return StatusCode.OK, prop_id
