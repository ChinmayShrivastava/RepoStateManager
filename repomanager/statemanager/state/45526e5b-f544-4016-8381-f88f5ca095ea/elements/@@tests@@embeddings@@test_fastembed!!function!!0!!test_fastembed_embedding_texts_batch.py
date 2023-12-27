def test_fastembed_embedding_texts_batch(
    model_name: str,
    max_length: int,
    doc_embed_type: Literal["default", "passage"],
    threads: int,
) -> None:
    """Test FastEmbed batch embedding."""
    documents = ["foo bar", "bar foo"]
    embedding = FastEmbedEmbedding(
        model_name=model_name,
        max_length=max_length,
        doc_embed_type=doc_embed_type,
        threads=threads,
    )

    output = embedding.get_text_embedding_batch(documents)
    assert len(output) == len(documents)
    assert len(output[0]) == 384
