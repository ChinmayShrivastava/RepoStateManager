class SimpleVectorStoreData(DataClassJsonMixin):
    """Simple Vector Store Data container.

    Args:
        embedding_dict (Optional[dict]): dict mapping node_ids to embeddings.
        text_id_to_ref_doc_id (Optional[dict]):
            dict mapping text_ids/node_ids to ref_doc_ids.

    """

    embedding_dict: Dict[str, List[float]] = field(default_factory=dict)
    text_id_to_ref_doc_id: Dict[str, str] = field(default_factory=dict)
    metadata_dict: Dict[str, Any] = field(default_factory=dict)
