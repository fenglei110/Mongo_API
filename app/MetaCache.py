# -*- coding: UTF-8 -*-
from app.MetaObject import PropertyTypes


class MetaCache:
    def __init__(self):
        self.entity = {}
        self.property = {}
        self.link = {}
        self.entity_idx = {}
        self.entity_prop_idx = {}
        self.link_idx = {}
        self.link_prop_idx = {}
        self.internal = {"name": PropertyTypes.STRING,
                         "desc": PropertyTypes.STRING,
                         "src": PropertyTypes.NUMBER,
                         "dest": PropertyTypes.NUMBER,
                         "typeid": PropertyTypes.NUMBER,
                         "timestamp": PropertyTypes.NUMBER,
                         "type": PropertyTypes.NUMBER}

    def upsert_entity(self, meta):
        """
        更改插入  实体
        entity = {64: {'m': '产品', 'p':{}, 'sl':[], 'dl':[]}}
        """
        if meta.id in self.entity:
            self.entity[meta.id]["m"] = meta
        else:
            self.entity[meta.id] = {"m": meta, "p": {}, "sl": [], "dl": []}

    def upsert_entity_prop(self, meta):
        """
        更改插入 实体/属性 映射
        entity_property = {64: {'m': '产品名称', 'p': {65: '产品'}, 'sl':[], 'dl':[]}}
        """
        if meta.elid in self.entity:
            self.entity[meta.elid]["p"][meta.id] = meta
            self.upsert_property(meta)

    def get_entity(self, id):
        return self.entity.get(id, None)

    def upsert_property(self, meta):
        """
        更改插入 属性
        property = {'65': '产品名称'}
        """
        self.property[meta.id] = meta

    def get_property(self, id):
        return self.property.get(id, None)

    def upsert_link(self, meta):
        """
        更改插入 关系
        link = {96: {'m': '子公司', 'p': {}}}
        """
        self.build_link_idx(meta.id, meta.name)
        self.build_link_idx(meta.id, meta.eng_name)
        if meta.id in self.link:
            self.link[meta.id]["m"] = meta
        else:
            self.link[meta.id] = {"m": meta, "p": {}}

        if meta.src_entity in self.entity:
            self.entity[meta.src_entity]["sl"].append(meta.id)

        if meta.dest_entity in self.entity:
            self.entity[meta.dest_entity]["dl"].append(meta.id)

    def get_link(self, id):
        return self.link.get(id, None)

    def upsert_link_prop(self, meta):
        """更改插入 关系/属性 映射"""
        if meta.elid in self.link:
            self.link[meta.elid]["p"][meta.id] = meta
            self.upsert_property(meta)
            self.build_link_prop_idx(meta.elid, meta.id, self.link[meta.elid]["m"].name, meta.name)
            self.build_link_prop_idx(meta.elid, meta.id, self.link[meta.elid]["m"].eng_name, meta.eng_name)

    def get_internal_type(self, id):
        return self.internal.get(id, None)

    def build_entity_idx(self, entity_id, entity_name):
        """
        entity_idx = {'公司':62, '人':63, '产品':64  ...}
        """
        self.entity_idx[entity_name] = entity_id

    def get_entity_idx(self, entity_name):
        return self.entity_idx.get(entity_name, None)

    def build_entity_prop_idx(self, entity_id, property_id, entity_name, property_name):
        """
        构建 实体/属性 映射
        entity_prop_idx = {'产品': {'产品名称': 65, '产品分类': 68}， '公司': {}, ...}
        """
        if entity_name not in self.entity_prop_idx:
            self.entity_prop_idx[entity_name] = {property_name: property_id}
        else:
            self.entity_prop_idx[entity_name][property_name] = property_id

    def get_entity_prop_idx(self, entity_name, property_name):
        if property_name not in self.entity_prop_idx.get(entity_name, {}):
            return None

        return self.entity_prop_idx[entity_name][property_name]

    def build_link_idx(self, link_id, link_name):
        """
        link_idx = {'子公司':96, '产品':98, '雇佣':99  ...}
        """
        self.link_idx[link_name] = link_id

    def get_link_idx(self, link_name):
        return self.link_idx.get(link_name, None)

    def build_link_prop_idx(self, link_id, property_id, link_name, property_name):
        """
        构建 属性/关系 映射
        link_prop_idx = {'控股': {'参股关系': 107， '参股比例': 108}, '子公司': {} ....}
        """
        if link_name not in self.entity_prop_idx:
            self.link_prop_idx[link_name] = {property_name: property_id}
        else:
            self.link_prop_idx[link_name][property_name] = property_id

    def get_link_prop_idx(self, link_name, property_name):
        if property_name not in self.link_prop_idx.get(link_name, {}):
            return None

        return self.link_prop_idx[link_name][property_name]

    def build_all(self):
        for k, v in self.entity.items():
            # k=64, v={'m': '产品', 'p':{}, 'sl':[], 'dl':[]}
            meta = v['m']
            self.build_entity_idx(meta['id'], meta['name'])
            self.build_entity_idx(meta['id'], meta['eng_name'])
            for pk, pv in v['p'].items():
                self.build_entity_prop_idx(meta['id'], pk, meta['name'], pv['name'])
                self.build_entity_prop_idx(meta['id'], pk, meta['eng_name'], pv['eng_name'])

        for k, v in self.link.items():
            meta = v['m']
            self.build_link_idx(meta['id'], meta['name'])
            self.build_link_idx(meta['id'], meta['eng_name'])
            for pk, pv in v['p'].items():
                self.build_link_prop_idx(meta['id'], pk, meta['name'], pv['name'])
                self.build_link_prop_idx(meta['id'], pk, meta['eng_name'], pv['eng_name'])
