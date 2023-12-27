def mock_service_context_merge_chunks(
    mock_service_context: ServiceContext,
) -> ServiceContext:
    def mock_repack(
        prompt_template: PromptTemplate, text_chunks: Sequence[str]
    ) -> List[str]:
        merged_chunks = []
        for chunks in zip(*[iter(text_chunks)] * 2):
            merged_chunks.append("\n".join(chunks))
        return merged_chunks

    mock_prompt_helper = Mock(spec=PromptHelper)
    mock_prompt_helper.repack.side_effect = mock_repack
    mock_service_context.prompt_helper = mock_prompt_helper
    return mock_service_context
