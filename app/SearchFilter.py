class FilterOperator:
    EQ = 0
    GTE = 1
    LT = 2
    IN = 3
    STRING_INCLUDE = 4
    NOT_NULL = 5


class SearchFilter(object):
    def __init__(self, col, op, value):
        self.col = col
        self.op = op
        self.value = value


class SearchFilters(object):
    def __init__(self):
        self.and_cond = []

    def add_and_filter(self, filter):
        self.and_cond.append(filter)

    def get_and_filters(self):
        return self.and_cond


