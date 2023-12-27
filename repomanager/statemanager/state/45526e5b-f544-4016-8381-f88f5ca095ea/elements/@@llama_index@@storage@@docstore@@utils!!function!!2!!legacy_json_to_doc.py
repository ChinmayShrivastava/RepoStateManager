def legacy_json_to_doc(doc_dict: dict) -> BaseNode:
    """Todo: Deprecated legacy support for old node versions."""
    doc_type = doc_dict[TYPE_KEY]
    data_dict = doc_dict[DATA_KEY]
    doc: BaseNode

    text = data_dict.get("text", "")
    metadata = data_dict.get("extra_info", {}) or {}
    id_ = data_dict.get("doc_id", None)

    relationships = data_dict.get("relationships", {})
    relationships = {
        NodeRelationship(k): RelatedNodeInfo(node_id=v)
        for k, v in relationships.items()
    }

    if doc_type == Document.get_type():
        doc = Document(
            text=text, metadata=metadata, id=id_, relationships=relationships
        )
    elif doc_type == TextNode.get_type():
        doc = TextNode(
            text=text, metadata=metadata, id=id_, relationships=relationships
        )
    elif doc_type == ImageNode.get_type():
        image = data_dict.get("image", None)
        doc = ImageNode(
            text=text,
            metadata=metadata,
            id=id_,
            relationships=relationships,
            image=image,
        )
    elif doc_type == IndexNode.get_type():
        index_id = data_dict.get("index_id", None)
        doc = IndexNode(
            text=text,
            metadata=metadata,
            id=id_,
            relationships=relationships,
            index_id=index_id,
        )
    else:
        raise ValueError(f"Unknown doc type: {doc_type}")

    return doc
