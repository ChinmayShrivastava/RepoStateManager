def convert_docs_to_json(nodes: List[BaseNode]) -> List[Dict]:
    """Convert docs to JSON."""
    docs = []
    for node in nodes:
        # TODO: add information for other fields as well
        # fields taken from
        # https://rb.gy/nmac9u
        doc_dict = {
            "id": node.node_id,
            "text": node.get_content(metadata_mode=MetadataMode.NONE),
            # NOTE: this is the doc_id to reference document
            "source_id": node.ref_doc_id,
            # "url": "...",
            # "created_at": ...,
            # "author": "..."",
        }
        metadata = node.metadata
        if metadata is not None:
            if "source" in metadata:
                doc_dict["source"] = metadata["source"]
            if "source_id" in metadata:
                doc_dict["source_id"] = metadata["source_id"]
            if "url" in metadata:
                doc_dict["url"] = metadata["url"]
            if "created_at" in metadata:
                doc_dict["created_at"] = metadata["created_at"]
            if "author" in metadata:
                doc_dict["author"] = metadata["author"]

        docs.append(doc_dict)
    return docs
