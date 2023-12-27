def legacy_metadata_dict_to_node(
    metadata: dict, text_key: str = DEFAULT_TEXT_KEY
) -> Tuple[dict, dict, dict]:
    """Common logic for loading Node data from metadata dict."""
    # make a copy first
    if metadata is None:
        metadata = {}
    else:
        metadata = metadata.copy()

    # load node_info from json string
    node_info_str = metadata.pop("node_info", "")
    if node_info_str == "":
        node_info = {}
    else:
        node_info = json.loads(node_info_str)

    # load relationships from json string
    relationships_str = metadata.pop("relationships", "")
    relationships: Dict[NodeRelationship, RelatedNodeInfo]
    if relationships_str == "":
        relationships = {}
    else:
        relationships = {
            NodeRelationship(k): RelatedNodeInfo(node_id=str(v))
            for k, v in json.loads(relationships_str).items()
        }

    # remove other known fields
    metadata.pop(text_key, None)
    metadata.pop("id", None)
    metadata.pop("document_id", None)
    metadata.pop("doc_id", None)
    metadata.pop("ref_doc_id", None)

    # remaining metadata is metadata or node_info
    new_metadata = {}
    for key, val in metadata.items():
        # NOTE: right now we enforce metadata to be dict of simple types.
        #       dump anything that's not a simple type into node_info.
        if isinstance(val, (str, int, float, type(None))):
            new_metadata[key] = val
        else:
            node_info[key] = val

    return new_metadata, node_info, relationships
