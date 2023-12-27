class MockLLMPredictor(BaseLLMPredictor):
    """Mock LLM Predictor."""

    max_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS, description="Number of tokens to mock generate."
    )

    _callback_manager: CallbackManager = PrivateAttr(default_factory=CallbackManager)

    @classmethod
    def class_name(cls) -> str:
        return "MockLLMPredictor"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata()

    @property
    def callback_manager(self) -> CallbackManager:
        return self.callback_manager

    @property
    def llm(self) -> LLM:
        raise NotImplementedError("MockLLMPredictor does not have an LLM model.")

    def predict(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        """Mock predict."""
        prompt_str = prompt.metadata["prompt_type"]
        if prompt_str == PromptType.SUMMARY:
            output = _mock_summary_predict(self.max_tokens, prompt_args)
        elif prompt_str == PromptType.TREE_INSERT:
            output = _mock_insert_predict()
        elif prompt_str == PromptType.TREE_SELECT:
            output = _mock_query_select()
        elif prompt_str == PromptType.TREE_SELECT_MULTIPLE:
            output = _mock_query_select_multiple(prompt_args["num_chunks"])
        elif prompt_str == PromptType.REFINE:
            output = _mock_refine(self.max_tokens, prompt, prompt_args)
        elif prompt_str == PromptType.QUESTION_ANSWER:
            output = _mock_answer(self.max_tokens, prompt_args)
        elif prompt_str == PromptType.KEYWORD_EXTRACT:
            output = _mock_keyword_extract(prompt_args)
        elif prompt_str == PromptType.QUERY_KEYWORD_EXTRACT:
            output = _mock_query_keyword_extract(prompt_args)
        elif prompt_str == PromptType.KNOWLEDGE_TRIPLET_EXTRACT:
            output = _mock_knowledge_graph_triplet_extract(
                prompt_args,
                int(prompt.kwargs.get("max_knowledge_triplets", 2)),
            )
        elif prompt_str == PromptType.CUSTOM:
            # we don't know specific prompt type, return generic response
            output = ""
        else:
            raise ValueError("Invalid prompt type.")

        return output

    def stream(self, prompt: BasePromptTemplate, **prompt_args: Any) -> TokenGen:
        raise NotImplementedError

    async def apredict(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        return self.predict(prompt, **prompt_args)

    async def astream(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> TokenAsyncGen:
        raise NotImplementedError
