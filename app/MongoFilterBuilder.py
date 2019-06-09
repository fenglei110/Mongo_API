from app.MetaObject import PropertyTypes


class MongoOpBuilder:
    def __init__(self):
        pass

    @staticmethod
    def op_eq(col, value, metaCache):
        v, internal = MongoOpBuilder.build_type(col, value, metaCache)
        return col, v, internal

    @staticmethod
    def op_gte(col, value, metaCache):
        v, internal = MongoOpBuilder.build_type(col, value, metaCache)
        return col, {"$gte": v}, internal

    @staticmethod
    def op_lt(col, value, metaCache):
        v, internal = MongoOpBuilder.build_type(col, value, metaCache)
        return col, {"$lt": v}, internal

    @staticmethod
    def op_in(col, value, metaCache):
        v, internal = MongoOpBuilder.build_type(col, value, metaCache)
        return col, {"$in": v}, internal

    @staticmethod
    def op_string_include(col, value, metaCache):
        v, internal = MongoOpBuilder.build_type(col, value, metaCache)
        return col, {"$regex": ".*%s.*" % value, "$options": "i"}, internal

    @staticmethod
    def op_not_null(col, value, metaCache):
        return col, {"$ne": ""}, False

    @staticmethod
    def build_type(col, value, metaCache):
        type = metaCache.get_internal_type(col)
        internal_type = True
        if type is None:
            p = metaCache.get_property(int(col))
            internal_type = False
            if p is None:
                type = PropertyTypes.STRING
            else:
                type = p.type

        if PropertyTypes.string(type):
            return value.encode("UTF-8"), internal_type

        # TODO : list
        return int(value), internal_type


class MongoFilterBuilder:
    def __init__(self):
        pass

    op = [MongoOpBuilder.op_eq,
          MongoOpBuilder.op_gte,
          MongoOpBuilder.op_lt,
          MongoOpBuilder.op_in,
          MongoOpBuilder.op_string_include,
          MongoOpBuilder.op_not_null]

    @staticmethod
    def build(filters, metaCache):
        query = {"$and": []}
        for f in filters.get_and_filters():
            col, m_filter, internal = MongoFilterBuilder.op[int(f.op)](f.col, f.value, metaCache)
            if internal:
                q = {col: m_filter}
            else:
                chs_col = "%s.c" % col
                eng_col = "%s.e" % col
                temp = []
                temp.append({chs_col: m_filter})
                temp.append({eng_col: m_filter})
                q = {"$or": temp}
            query["$and"].append(q)
        return query
