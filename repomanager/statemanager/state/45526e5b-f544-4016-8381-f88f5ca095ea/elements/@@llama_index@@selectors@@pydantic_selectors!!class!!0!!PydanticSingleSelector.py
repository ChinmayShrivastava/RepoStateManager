class PydanticSingleSelector(BaseSelector):
    def __init__(self, selector_program: BasePydanticProgram) -> None:
        self._selector_program = selector_program

    @classmethod
    def from_defaults(
        cls,
        program: Optional[BasePydanticProgram] = None,
        llm: Optional[OpenAI] = None,
        prompt_template_str: str = DEFAULT_SINGLE_PYD_SELECT_PROMPT_TMPL,
        verbose: bool = False,
    ) -> "PydanticSingleSelector":
        if program is None:
            program = OpenAIPydanticProgram.from_defaults(
                output_cls=SingleSelection,
                prompt_template_str=prompt_template_str,
                llm=llm,
                verbose=verbose,
            )

        return cls(selector_program=program)

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
        choices_text = _build_choices_text(choices)

        # predict
        prediction = self._selector_program(
            num_choices=len(choices),
            context_list=choices_text,
            query_str=query.query_str,
        )

        # parse output
        return _pydantic_output_to_selector_result(prediction)

    async def _aselect(
        self, choices: Sequence[ToolMetadata], query: QueryBundle
    ) -> SelectorResult:
        raise NotImplementedError(
            "Async selection not supported for Pydantic Selectors."
        )