def test_resolve_embed_model(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.embeddings.huggingface.HuggingFaceEmbedding.__init__",
        mock_hf_embeddings,
    )
    monkeypatch.setattr(
        "llama_index.embeddings.OpenAIEmbedding.__init__", mock_openai_embeddings
    )

    # Test None
    embed_model = resolve_embed_model(None)
    assert isinstance(embed_model, MockEmbedding)

    # Test str
    embed_model = resolve_embed_model("local")
    assert isinstance(embed_model, HuggingFaceEmbedding)

    # Test LCEmbeddings
    embed_model = resolve_embed_model(HuggingFaceEmbedding())
    assert isinstance(embed_model, HuggingFaceEmbedding)

    # Test BaseEmbedding
    embed_model = resolve_embed_model(OpenAIEmbedding())
    assert isinstance(embed_model, OpenAIEmbedding)