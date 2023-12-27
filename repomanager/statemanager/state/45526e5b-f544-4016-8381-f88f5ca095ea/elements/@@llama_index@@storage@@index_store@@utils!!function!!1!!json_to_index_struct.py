def json_to_index_struct(struct_dict: dict) -> IndexStruct:
    type = struct_dict[TYPE_KEY]
    data_dict = struct_dict[DATA_KEY]
    cls = INDEX_STRUCT_TYPE_TO_INDEX_STRUCT_CLASS[type]
    try:
        return cls.from_json(data_dict)
    except TypeError:
        return cls.from_dict(data_dict)
