def test_get_chunk_size(
    prompt: str,
    chunk_size_limit: Optional[int],
    num_chunks: int,
    padding: int,
    expected: Union[int, Type[Exception]],
) -> None:
    """Test get chunk size given prompt."""
    prompt_helper = PromptHelper(
        context_window=11,
        num_output=1,
        chunk_overlap_ratio=0,
        tokenizer=mock_tokenizer,
        chunk_size_limit=chunk_size_limit,
    )
    if isinstance(expected, int):
        chunk_size = prompt_helper._get_available_chunk_size(
            PromptTemplate(prompt), num_chunks, padding=padding
        )
        assert chunk_size == expected
    else:
        with pytest.raises(expected):
            prompt_helper._get_available_chunk_size(
                PromptTemplate(prompt), num_chunks, padding=padding
            )
