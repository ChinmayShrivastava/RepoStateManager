def json_to_doc(doc_dict: dict) -> BaseNode:
    doc_type = doc_dict[TYPE_KEY]
    data_dict = doc_dict[DATA_KEY]
    doc: BaseNode

    if "extra_info" in data_dict:
        return legacy_json_to_doc(doc_dict)
    else:
        if doc_type == Document.get_type():
            doc = Document.parse_obj(data_dict)
        elif doc_type == ImageDocument.get_type():
            doc = ImageDocument.parse_obj(data_dict)
        elif doc_type == TextNode.get_type():
            doc = TextNode.parse_obj(data_dict)
        elif doc_type == ImageNode.get_type():
            doc = ImageNode.parse_obj(data_dict)
        elif doc_type == IndexNode.get_type():
            doc = IndexNode.parse_obj(data_dict)
        else:
            raise ValueError(f"Unknown doc type: {doc_type}")

        return doc
