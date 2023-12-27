class LLMMultiSelector(BaseSelector):
    """LLM multi selector.

    LLM-based selector that chooses multiple out of many options.

    Args:
        llm (LLM): An LLM.
        prompt (SingleSelectPrompt): A LLM prompt for selecting multiple out of many
            options.
    """

    def __init__(
        self,
        llm: LLMPredictorType,
        prompt: MultiSelectPrompt,
        max_outputs: Optional[int] = None,
    ) -> None:
        self._llm = llm
        self._prompt = prompt
        self._max_outputs = max_outputs

        if self._prompt.output_parser is None:
            raise ValueError("Prompt should have output parser.")

    @classmethod
    def from_defaults(
        cls,
        service_context: Optional[ServiceContext] = None,
        prompt_template_str: Optional[str] = None,
        output_parser: Optional[BaseOutputParser] = None,
        max_outputs: Optional[int] = None,
    ) -> "LLMMultiSelector":
        service_context = service_context or ServiceContext.from_defaults()
        prompt_template_str = prompt_template_str or DEFAULT_MULTI_SELECT_PROMPT_TMPL
        output_parser = output_parser or SelectionOutputParser()

        # add output formatting
        prompt_template_str = output_parser.format(prompt_template_str)

        # construct prompt
        prompt = MultiSelectPrompt(
            template=prompt_template_str,
            output_parser=output_parser,
            prompt_type=PromptType.MULTI_SELECT,
        )
        return cls(service_context.llm, prompt, max_outputs)

    def _get_prompts(self) -> Dict[str, Any]:
        """Get prompts."""
        return {"prompt": self._prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "prompt" in prompts:
            self._prompt = prompts["prompt"]

    def _select(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        # prepare input
        context_list = _build_choices_text(choices)
        max_outputs = self._max_outputs or len(choices)

        prediction = self._llm.predict(
            prompt=self._prompt,
            num_choices=len(choices),
            max_outputs=max_outputs,
            context_list=context_list,
            query_str=query.query_str,
        )

        assert self._prompt.output_parser is not None
        parsed = self._prompt.output_parser.parse(prediction)
        return _structured_output_to_selector_result(parsed)

    async def _aselect(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        # prepare input
        context_list = _build_choices_text(choices)
        max_outputs = self._max_outputs or len(choices)

        prediction = await self._llm.apredict(
            prompt=self._prompt,
            num_choices=len(choices),
            max_outputs=max_outputs,
            context_list=context_list,
            query_str=query.query_str,
        )

        assert self._prompt.output_parser is not None
        parsed = self._prompt.output_parser.parse(prediction)
        return _structured_output_to_selector_result(parsed)
