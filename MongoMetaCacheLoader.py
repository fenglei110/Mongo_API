from MetaCacheLoader import MetaCacheLoader
from MetaCache import MetaCache
from MetaObject import EntityMeta, PropertyMeta, LinkMeta


class MongoMetaCacheLoader(MetaCacheLoader):
    def __init__(self, meta_operator):
        self.meta_operator = meta_operator

    def load(self):
        meta = MetaCache()
        for i in self.meta_operator.get_all_entities():
            e = EntityMeta()
            e.from_json(i, False)
            meta.upsert_entity(e)

        for i in self.meta_operator.get_all_entity_props():
            p = PropertyMeta()
            p.from_json(i, False)
            meta.upsert_entity_prop(p)

        for i in self.meta_operator.get_all_links():
            l = LinkMeta()
            l.from_json(i, False)
            meta.upsert_link(l)

        for i in self.meta_operator.get_all_link_props():
            p = PropertyMeta()
            p.from_json(i, False)
            meta.upsert_link_prop(p)

        return meta
