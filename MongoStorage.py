# coding=utf-8
import json
import logging

from pymongo import MongoClient, ReturnDocument

from AbstractStorage import AbstractStorage


class MongoStorage(AbstractStorage):
    """mongo交互"""
    def __init__(self, conf):
        self.conf = conf
        self.__conn()

    def __conn(self):
        self.client = MongoClient(self.conf.url)
        self.db = self.client[self.conf.db]
        logging.info('%s connected', self.conf)

    def get_all(self, table, *args):
        """
        projection={"_id": False})  返回结果中 drop  _id
        :param table:
        :return:
        """
        res = self.db[table].find(projection={"_id": False})
        return res

    def get_by_id(self, table, id):
        """by id"""
        res = self.db[table].find_one({'id': id}, projection={"_id": False})
        return res

    def get_by_query(self, table, kvs):
        """by 其他条件"""
        res = self.db[table].find(kvs, projection={"_id": False})
        return res

    def get_by_query_limit(self, table, kvs, size):
        res = self.db[table].find(kvs, projection={"_id": False}).limit(size)
        return res

    def put(self, table, kvs):
        """insert_one"""
        self.db[table].insert_one(kvs)

    def get_multi(self, table, key):
        pass

    def update(self, table, id, value):
        """find_one_and_update"""
        res = self.db[table].find_one_and_update({'id': id}, {"$set": value}, upsert=False)
        return res

    def update_mutil_key(self, table, keys, value):
        res = self.db[table].find_one_and_update(keys, {"$set": value}, upsert=False)
        return res

    def update_push(self, table, id, value):
        res = self.db[table].find_one_and_update({'id': id}, {"$push": value}, upsert=False)
        return res

    def update_pull(self, table, id, value):
        res = self.db[table].find_one_and_update({'id': id}, {"$pull": value}, upsert=False)
        return res

    def delete_by_id(self, table, key):
        return self.db[table].delete_many({'id': key})

    def delete_by_query(self, table, query):
        return self.db[table].delete_many(query)

    def aggregate(self, table, querys):
        """对查询结果聚合"""
        querys.append({"$project": {"_id": 0}})
        logging.info(json.dumps(querys))
        return self.db[table].aggregate(querys)

    def gen_id(self, table):
        """
        id累加 1
        ReturnDocument.AFTER  返回修改后的结果
        {'id': True, '_id': False}  只返回id
        :param table: table name
        :return: id
        """
        id = self.db[table].find_one_and_update({"_id": "accumulator"}, {"$inc": {"id": 1}},
                                                projection={'id': True, '_id': False},
                                                upsert=True,
                                                return_document=ReturnDocument.AFTER)

        return id["id"]
