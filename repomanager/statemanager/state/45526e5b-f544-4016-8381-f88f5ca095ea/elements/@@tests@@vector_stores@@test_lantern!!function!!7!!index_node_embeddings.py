def index_node_embeddings() -> List[TextNode]:
    return [
        TextNode(
            text="lorem ipsum",
            id_="aaa",
            embedding=_get_sample_vector(0.1),
        ),
        TextNode(
            text="dolor sit amet",
            id_="bbb",
            extra_info={"test_key": "test_value"},
            embedding=_get_sample_vector(1.0),
        ),
        IndexNode(
            text="The quick brown fox jumped over the lazy dog.",
            id_="aaa_ref",
            index_id="aaa",
            embedding=_get_sample_vector(5.0),
        ),
    ]
