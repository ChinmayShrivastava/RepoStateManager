def patch_token_text_splitter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(SentenceSplitter, "split_text", patch_token_splitter_newline)
    monkeypatch.setattr(
        SentenceSplitter,
        "split_text_metadata_aware",
        patch_token_splitter_newline,
    )
    monkeypatch.setattr(TokenTextSplitter, "split_text", patch_token_splitter_newline)
    monkeypatch.setattr(
        TokenTextSplitter, "split_text_metadata_aware", patch_token_splitter_newline
    )
