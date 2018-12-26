from webargs import fields


class Argument:
    all_items_in_cache = {
        '_id': fields.Str(required=True),
    }

    single_items_in_cache = {
        '_id': fields.Str(required=True),
        'urls': fields.Str(required=True),
    }
