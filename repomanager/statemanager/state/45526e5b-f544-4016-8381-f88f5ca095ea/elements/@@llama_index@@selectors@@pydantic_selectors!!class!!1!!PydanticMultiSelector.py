class PydanticMultiSelector(BaseSelector):
    def __init__(
        self, selector_program: BasePydanticProgram, max_outputs: Optional[int] = None
    ) -> None:
        self._selector_program = selector_program
        self._max_outputs = max_outputs

    @classmethod
    def from_defaults(
        cls,
        program: Optional[BasePydanticProgram] = None,
        llm: Optional[OpenAI] = None,
        prompt_template_str: str = DEFAULT_MULTI_PYD_SELECT_PROMPT_TMPL,
        max_outputs: Optional[int] = None,
        verbose: bool = False,
    ) -> "PydanticMultiSelector":
        if program is None:
            program = OpenAIPydanticProgram.from_defaults(
                output_cls=MultiSelection,
                prompt_template_str=prompt_template_str,
                llm=llm,
                verbose=verbose,
            )

        return cls(selector_program=program, max_outputs=max_outputs)

    def _get_prompts(self) -> Dict[str, Any]:
        """Get prompts."""
        # TODO: no accessible prompts for a base pydantic program
        return {}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""

    def _select(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        # prepare input
        context_list = _build_choices_text(choices)
        max_outputs = self._max_outputs or len(choices)

        # predict
        prediction = self._selector_program(
            num_choices=len(choices),
            max_outputs=max_outputs,
            context_list=context_list,
            query_str=query.query_str,
        )

        # parse output
        return _pydantic_output_to_selector_result(prediction)

    async def _aselect(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        return self._select(choices, query)
