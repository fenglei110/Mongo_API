#!/usr/bin/env python
# coding=utf-8

import json
import logging
import sys
from importlib import reload

from bson import json_util
from flask import Flask, request, abort

from app.Accumulator import Accumulator
from app.DataOperator import DataOperator
from app.DataReplicaOperator import DataReplicaOperator
from app.MetaOperator import MetaOperator
from app.MongoMetaCacheLoader import MongoMetaCacheLoader
from app.MongoSearcher import MongoSearcher
from app.MongoStorage import MongoStorage
from app.SearchFilter import SearchFilter, SearchFilters
from app.StatusCode import StatusCode
from app.StorageConf import StorageConf
from app.TableConf import TableConf

reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


# ------------  meta  ------------
storageConf = StorageConf('mongodb://feng:123456@127.57.40.140:29017/test_meta', 'test_meta', 'test_meta')

"""连接mongo, url, db, table"""
storage = MongoStorage(storageConf)
# 实例化累加器
accumulator = Accumulator(storage)
tableConf = TableConf("entity", "link", "property", "entity_property", "link_property")
meta = MetaOperator(storage, accumulator, tableConf, None)

cacheLoader = MongoMetaCacheLoader(meta)
metaCache = cacheLoader.load()

meta.meta_cache = metaCache

# ------------  data -----------
dataStorageConf = StorageConf('mongodb://localhost:29017/test_meta', 'test_meta', 'test_meta')
dataStorage = MongoStorage(dataStorageConf)
dataAccumulator = Accumulator(dataStorage)

dataTableConf = TableConf("entity", "link", "property", None, None)
dataOrginOperator = DataOperator(dataStorage, dataAccumulator, metaCache, dataTableConf)

dataRepStorageConf = StorageConf('mongodb://feng:123456@127.57.40.140:29017/test_fact', 'test_fact', 'test_fact')
dataRepStorage = MongoStorage(dataRepStorageConf)

dataRepTableConf = TableConf("entity", "link", None, None, None)
dataReqOperator = DataReplicaOperator(dataStorage, dataRepStorage, dataAccumulator, metaCache, dataTableConf,
                                      dataRepTableConf)

dataOperator = dataReqOperator

searcher = MongoSearcher(dataRepStorage, dataRepTableConf, metaCache)


@app.route('/meta/entity')
def all_entites():
    try:
        res = meta.get_all_entities()
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/entity/<entity_id>', methods=['GET'])
def get_entity(entity_id):
    try:
        res = meta.get_entity(entity_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/entity_search', methods=['GET'])
def search_entity(entity_id):
    if not request.json or 'name' not in request.json:
        abort(400)
    try:
        res = meta.get_eneity_by_name(request.json['name'])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/entity', methods=['POST'])
def insert_meta_entity():
    j = json.loads(request.get_data())

    if not j:
        abort(400)
    try:
        res = meta.put_entity(j['name'], j['eng_name'], j['desc'], j['eng_desc'], j['pid'])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(res))


@app.route('/meta/entity/<entity_id>', methods=['DELETE'])
def delete_meta_entity(entity_id):
    try:
        meta.delete_entity(entity_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return


@app.route('/meta/link')
def all_links():
    try:
        res = meta.get_all_links()
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/link/<link_id>', methods=['GET'])
def get_link(link_id):
    try:
        res = meta.get_link(int(link_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/link', methods=['POST'])
def insert_meta_link():
    j = json.loads(request.get_data())

    if not j:
        abort(400)
    try:
        res = meta.put_link(j['name'],
                            j['eng_name'],
                            j['desc'],
                            j['eng_desc'],
                            j['pid'],
                            j['src_entity'],
                            j['dest_entity'])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(res))


@app.route('/meta/link/<link_id>', methods=['DELETE'])
def delete_link_entity(link_id):
    try:
        meta.delete_link(link_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return


@app.route('/meta/entity/<entity_id>/property', methods=['GET'])
def get_entity_prop(entity_id):
    try:
        res = meta.get_entity_prop(int(entity_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/entity/<entity_id>/property', methods=['POST'])
def put_entity_prop(entity_id):
    if not request.json:
        abort(400)
    j = request.json
    try:
        res = meta.put_entity_prop(j["name"],
                                   j["eng_name"],
                                   j["desc"],
                                   j["eng_desc"],
                                   int(entity_id),
                                   j["type"],
                                   j["number_of_value"],
                                   None if 'enum_value' not in j else j['enum_value'],
                                   None if 'eng_enum_value' not in j else j['eng_enum_value'])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(res))


@app.route('/meta/entity/<entity_id>/property/<prop_id>', methods=['DELETE'])
def delete_meta_entity_prop(prop_id):
    try:
        meta.delete_entity_prop(prop_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return


@app.route('/meta/link/<link_id>/property', methods=['GET'])
def get_link_prop(link_id):
    try:
        res = meta.get_link_prop(int(link_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/link/<link_id>/property', methods=['POST'])
def put_link_prop(link_id):
    if not request.json:
        abort(400)
    j = request.json
    try:
        res = meta.put_link_prop(j["name"],
                                 j["eng_name"],
                                 j["desc"],
                                 j["eng_desc"],
                                 int(link_id),
                                 j["type"],
                                 j["number_of_value"],
                                 None if 'enum_value' not in j else j['enum_value'],
                                 None if 'eng_enum_value' not in j else j['eng_enum_value'])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(res))


@app.route('/meta/link/<link_id>/property/<prop_id>', methods=['DELETE'])
def delete_meta_link_prop(prop_id):
    try:
        meta.delete_link_prop(prop_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return


@app.route('/meta/property/<property_id>', methods=['GET'])
def get_property(property_id):
    try:
        res = meta.get_link(property_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, res)


@app.route('/meta/properties', methods=['POST'])
def insert_meta_prop():
    if not request.json:
        abort(400)
    j = request.json

    if not j:
        abort(400)
    try:
        res = meta.put_property(j['name'],
                                j['desc'],
                                j['type'],
                                None if 'enum_value' not in j else j['enum_value'])

    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(res))


@app.route('/meta/metas')
def get_all_metas():
    return json.dumps(metaCache, default=lambda o: o.__dict__, ensure_ascii=False)


@app.route('/data/entity/<entity_id>', methods=['GET'])
def get_data_entity(entity_id):
    try:
        res = dataOperator.get_entity_by_id(int(entity_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_bson_result(200, res)


@app.route('/data/entity_property/<entity_id>', methods=['GET'])
def get_data_entity_property(entity_id):
    try:
        res = dataOperator.get_property(int(entity_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_bson_result(200, res)


@app.route('/data/entity', methods=['GET'])
def get_data_all_entity():
    start = int(request.args.get('start', '0'))
    size = int(request.args.get('size', '100'))
    q = [{"col": "typeid", "op": 0, "value": int(request.args.get('typeid', 0))}]

    try:
        res = searcher.SearchEntity(build_filter(q),
                                    start,
                                    size)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_bson_result(200, res)


@app.route('/data/entity', methods=['POST'])
def put_data_entity():
    if not request.json:
        abort(400)
    j = request.json
    try:
        id = dataOperator.put_entity(j["name"],
                                     j["eng_name"],
                                     j["typeid"])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(id))


@app.route('/data/link/<link_id>', methods=['GET'])
def get_data_link(link_id):
    try:
        res = dataOperator.get_link_by_id(link_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(res))


@app.route('/data/link', methods=['GET'])
def get_data_all_link():
    start = int(request.args.get('start', '0'))
    size = int(request.args.get('size', '100'))
    q = [{"col": "typeid", "op": 0, "value": int(request.args.get('typeid', 0))}]

    try:
        res = searcher.SearchLink(build_filter(q),
                                  start,
                                  size)
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_bson_result(200, res)


@app.route('/data/link', methods=['POST'])
def put_data_link():
    j = json.loads(request.get_data())

    if not j:
        abort(400)
    try:
        id = dataOperator.put_link(j["src"],
                                   j["dest"],
                                   j["typeid"])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(id))


@app.route('/data/property', methods=['POST'])
def put_data_property():
    j = json.loads(request.get_data())

    if not j:
        abort(400)
    try:
        code, id = dataOperator.put_property(j["elid"],
                                             j["typeid"],
                                             j["value"],
                                             j["eng_value"],
                                             j["is_entity"])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_result(200, gen_id_result(id))


@app.route('/data/entity/<entity_id>', methods=['PUT'])
def update_data_entity(entity_id):
    if not request.json:
        abort(400)
    j = request.json
    try:
        code, id = dataOperator.update_entity(
            int(entity_id),
            None if 'name' not in j else j['name'],
            None if 'eng_name' not in j else j['eng_name'])
        if code != StatusCode.OK:
            logging.error("%s update failed:not exists" % entity_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(id))


@app.route('/data/property/<prop_id>', methods=['PUT'])
def update_data_property(prop_id):
    if not request.json:
        abort(400)

    j = request.json
    try:
        code, id = dataOperator.update_property(int(prop_id),
                                                None if 'value' not in j else j['value'],
                                                None if 'eng_value' not in j else j['eng_value'])

        if code != StatusCode.OK:
            logging.error("%s update failed:not exists" % prop_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(id))


@app.route('/data/property/<prop_id>', methods=['DELETE'])
def delete_data_property(prop_id):
    try:
        code, id = dataOperator.delete_property(int(prop_id))

        if code != StatusCode.OK:
            logging.error("%s delete failed:not exists" % prop_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(id))


@app.route('/data/entity/<entity_id>', methods=['DELETE'])
def delete_data_entity(entity_id):
    try:
        code, id = dataOperator.delete_entity(int(entity_id))

        if code != StatusCode.OK:
            logging.error("%s delete failed:not exists" % entity_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(id))


@app.route('/data/link/<link_id>', methods=['DELETE'])
def delete_data_link(link_id):
    try:
        code, id = dataOperator.delete_link(int(link_id))

        if code != StatusCode.OK:
            logging.error("%s delete failed:not exists" % link_id)
    except Exception as e:
        app.log_exception(e)
        abort(500)

    return gen_result(200, gen_id_result(id))


@app.route('/search/entity', methods=['POST'])
def data_entity_search():
    if not request.json:
        abort(400)
    try:
        res = searcher.SearchEntity(build_filter(request.json["q"]),
                                    request.json["start"],
                                    request.json["size"])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_bson_result(200, res)


@app.route('/search/property', methods=['POST'])
def data_property_search():
    pass


@app.route('/search/link', methods=['POST'])
def data_link_search():
    if not request.json:
        abort(400)
    try:
        res = searcher.SearchLink(build_filter(request.json["q"]),
                                  request.json["start"],
                                  request.json["size"])
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_bson_result(200, res)


@app.route('/search/entitylink/<entity_id>', methods=['GET'])
def data_entity_link_search(entity_id):
    try:
        res = searcher.SearchBothLinkById(int(entity_id))
    except Exception as e:
        app.log_exception(e)
        abort(500)
    return gen_bson_result(200, res)


def gen_result(code, data):
    # return json.dumps({"code": code, "data": "%s" % data}, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def gen_bson_result(code, data):
    # return json.dumps({"code": code, "data": "%s" % data}, ensure_ascii=False)
    return json_util.dumps(data, ensure_ascii=False)


def gen_id_result(id):
    return {"id": id}


def build_filter(f):
    filters = SearchFilters()
    for i in f:
        filters.add_and_filter(SearchFilter(i["col"], i["op"], i["value"]))
    return filters


if __name__ == '__main__':
    app.run()
