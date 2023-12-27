def index_struct_to_json(index_struct: IndexStruct) -> dict:
    return {
        TYPE_KEY: index_struct.get_type(),
        DATA_KEY: index_struct.to_json(),
    }
