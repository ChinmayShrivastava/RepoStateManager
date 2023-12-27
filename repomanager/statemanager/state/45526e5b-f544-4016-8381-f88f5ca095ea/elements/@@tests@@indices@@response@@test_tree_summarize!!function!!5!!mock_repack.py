    def mock_repack(
        prompt_template: PromptTemplate, text_chunks: Sequence[str]
    ) -> List[str]:
        merged_chunks = []
        for chunks in zip(*[iter(text_chunks)] * 2):
            merged_chunks.append("\n".join(chunks))
        return merged_chunks
