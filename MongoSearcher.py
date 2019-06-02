# -*- coding: UTF-8 -*-

from Seracher import Searcher
from MongoFilterBuilder import MongoFilterBuilder
from SearchFilter import *


class MongoSearcher(Searcher):
    def __init__(self, storage, tableConf, metaCache):
        self.storage = storage
        self.entity_table = tableConf.entity_table
        self.link_table = tableConf.link_table
        self.metaCache = metaCache

    def SearchEntity(self, filters, start, size):
        return self.__search(self.entity_table, self.__build(filters, start, size))

    def SearchBothLinkById(self, id):

        src_pip = []
        src_pip.append({"$match": {"src": id}})
        src_pip.append({
            "$lookup": {"from": self.entity_table, "localField": "dest", "foreignField": "id", "as": "dest_detail"}})

        dest_pip = []
        dest_pip.append({"$match": {"dest": id}})
        dest_pip.append({
            "$lookup": {"from": self.entity_table, "localField": "src", "foreignField": "id", "as": "src_detail"}})

        facet = {"$facet": {"src": src_pip, "dest": dest_pip}}
        r = self.__search(self.link_table, [facet])

        for i in r:
            result = i
            break

        r = self.storage.get_by_id(self.entity_table, id)
        if r is None:
            r = {}
        result["self"] = r
        return result

    def SearchLink(self, filters, start, size):
        pip = self.__build(filters, start, size)
        src_detail = {
            "$lookup": {"from": self.entity_table, "localField": "src", "foreignField": "id", "as": "src_detail"}}
        dest_detail = {
            "$lookup": {"from": self.entity_table, "localField": "dest", "foreignField": "id", "as": "dest_detail"}}
        pip.append(src_detail)
        pip.append(dest_detail)
        return self.__search(self.link_table, pip)

    def __build(self, filters, start, size):
        query = MongoFilterBuilder.build(filters, self.metaCache)
        query["id"] = {"$gte": start}
        limit = {"$limit": size}
        pip = [{"$match": query}, limit]
        return pip

    def __search(self, table, pip):
        return self.storage.aggregate(table, pip)
