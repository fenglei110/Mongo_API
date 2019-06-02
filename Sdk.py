#!/usr/bin/env python
# -*-coding:utf-8 -*-


import json

import requests

from DataObject import LinkData, EntityData
from MetaCache import MetaCache
from MetaObject import EntityMeta, LinkMeta, PropertyMeta


class KnowledgeReactorSdk:
    ALL_METAS = "/meta/metas"
    ENTITY_META = "/meta/entity"
    ENTITY_PROP_METAS = "/meta/entity/%s/property"
    ENTITY_PROP_META = "/meta/entity/%s/property/%s"

    LINK_META = "/meta/link"
    LINK_PROP_METAS = "/meta/link/%d/property"
    LINK_PROP_META = "/meta/link/%d/property/%s"

    ENTITY_DATA = "/data/entity"
    ENTITY_PROP_DATA = "/data/entity_property"
    PROP_DATA = "/data/property"
    LINK_DATA = "/data/link"
    LINK_PROP_DATA = "/data/link_property"
    PROP_DATA_ID = "/data/property/%s"

    def __init__(self, url, timeout=1):
        self.url = url
        self.timeout = timeout

    def __get(self, url):
        """get"""
        r = requests.get(self.__gen_url(url))
        r.raise_for_status()
        return r.json()

    def __put(self, url, data):
        """put"""
        headers = {'content-type': 'application/json'}
        r = requests.put(self.__gen_url(url), data=json.dumps(data, default=lambda o: o.__dict__), headers=headers)
        r.raise_for_status()
        return r.json()

    def __post(self, url, data):
        """post"""
        headers = {'content-type': 'application/json'}
        r = requests.post(self.__gen_url(url), data=json.dumps(data, default=lambda o: o.__dict__), headers=headers)
        r.raise_for_status()
        return r.json()

    def __delete(self, url):
        """delete"""
        r = requests.delete(self.__gen_url(url))
        r.raise_for_status()

    def __gen_url(self, uri):
        """url拼接"""
        return self.url + uri

    ########## meta ########

    def get_all_meta(self):
        res = self.__get(self.ALL_METAS)
        meta_cache = MetaCache()
        meta_cache.__dict__.update(res)
        meta_cache.build_all()
        return meta_cache

    def get_entity_meta(self, id):
        res = self.__get(self.ENTITY_META + "/%s" % id)
        meta = EntityMeta()
        meta.from_json(res)
        return meta

    def put_entity_meta(self, entity_meta):
        res = self.__post(self.ENTITY_META, entity_meta)
        return res["id"]

    def get_link_meta(self, id):
        res = self.__get(self.LINK_META + "/%s" % id)
        meta = LinkMeta()
        meta.from_json(res)
        return meta

    def put_link_meta(self, link_meta):
        res = self.__post(self.LINK_META, link_meta)
        return res["id"]

    def get_entity_property_meta(self, entity_id):
        res = self.__get(self.ENTITY_PROP_METAS % entity_id)
        metas = []
        for i in res:
            p = PropertyMeta()
            p.from_json(i)
            metas.append(p)
        return metas

    def put_entity_property_meta(self, entity_id, ep):
        res = self.__post(self.ENTITY_PROP_METAS % entity_id, ep)
        return res["id"]

    def get_link_property_meta(self, link_id):
        res = self.__get(self.LINK_PROP_METAS % link_id)
        metas = []
        for i in res:
            p = PropertyMeta()
            p.from_json(i)
            metas.append(p)
        return metas

    def put_link_property_meta(self, link_id, lp):
        res = self.__post(self.LINK_PROP_METAS % link_id, lp)
        return res["id"]

    ################# data ##################

    def get_entity_data(self, entity_id):
        res = self.__get(self.ENTITY_DATA + "/%s" % entity_id)
        data = EntityData()
        data.from_json(res)
        return data

    def put_entity_data(self, data):
        res = self.__post(self.ENTITY_DATA, data)
        return res["id"]

    def get_link_data(self, link_id):
        res = self.__get(self.LINK_DATA + "/%s" % link_id)
        data = LinkData()
        data.from_json(res)
        return data

    def put_link_data(self, data):
        res = self.__post(self.LINK_DATA, data)
        return res["id"]

    def put_entity_prop_data(self, prop):
        t = prop.to_json()
        t["is_entity"] = True
        res = self.__post(self.PROP_DATA, t)
        return res["id"]

    def put_link_prop_data(self, prop):
        t = prop.to_json()
        t["is_entity"] = False
        res = self.__post(self.PROP_DATA, t)
        return res["id"]

    def modify_prop_data(self, prop_id, prop):
        t = prop.to_json()
        res = self.__put(self.PROP_DATA_ID % prop_id, t)
        return res["id"]


if __name__ == '__main__':
    kr = KnowledgeReactorSdk("http://127.0.0.1:5000")
    # print json.dumps(kr.get_all_meta(), default=lambda o: o.__dict__, ensure_ascii=False)

    print(json.dumps(kr.get_entity_meta("20").to_json(), ensure_ascii=False))
    print(json.dumps(kr.get_link_meta("27").to_json(), ensure_ascii=False))
    """
    meta = PropertyMeta(name="性别", 
                        eng_name="sex", 
                        desc="性别", 
                        eng_desc="sex", 
                        elid=21, 
                        type="enum_string", 
                        enum_value=["男","女"], 
                        eng_enum_value=["male", "female"], 
                        number_of_value=0)
    """
    print(json.dumps(kr.get_entity_property_meta("21"), default=lambda o: o.__dict__, ensure_ascii=False))
    print(json.dumps(kr.get_entity_data("31"), default=lambda o: o.__dict__, ensure_ascii=False))
