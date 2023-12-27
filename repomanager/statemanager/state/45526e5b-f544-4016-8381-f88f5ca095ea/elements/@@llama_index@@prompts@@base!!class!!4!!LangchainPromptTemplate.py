class LangchainPromptTemplate(BasePromptTemplate):
    selector: Any
    requires_langchain_llm: bool = False

    def __init__(
        self,
        template: Optional["LangchainTemplate"] = None,
        selector: Optional["LangchainSelector"] = None,
        output_parser: Optional[BaseOutputParser] = None,
        prompt_type: str = PromptType.CUSTOM,
        metadata: Optional[Dict[str, Any]] = None,
        template_var_mappings: Optional[Dict[str, Any]] = None,
        function_mappings: Optional[Dict[str, Callable]] = None,
        requires_langchain_llm: bool = False,
    ) -> None:
        try:
            from llama_index.bridge.langchain import (
                ConditionalPromptSelector as LangchainSelector,
            )
        except ImportError:
            raise ImportError(
                "Must install `llama_index[langchain]` to use LangchainPromptTemplate."
            )
        if selector is None:
            if template is None:
                raise ValueError("Must provide either template or selector.")
            selector = LangchainSelector(default_prompt=template)
        else:
            if template is not None:
                raise ValueError("Must provide either template or selector.")
            selector = selector

        kwargs = selector.default_prompt.partial_variables
        template_vars = selector.default_prompt.input_variables

        if metadata is None:
            metadata = {}
        metadata["prompt_type"] = prompt_type

        super().__init__(
            selector=selector,
            metadata=metadata,
            kwargs=kwargs,
            template_vars=template_vars,
            output_parser=output_parser,
            template_var_mappings=template_var_mappings,
            function_mappings=function_mappings,
            requires_langchain_llm=requires_langchain_llm,
        )

    def partial_format(self, **kwargs: Any) -> "BasePromptTemplate":
        """Partially format the prompt."""
        from llama_index.bridge.langchain import (
            ConditionalPromptSelector as LangchainSelector,
        )

        mapped_kwargs = self._map_all_vars(kwargs)
        default_prompt = self.selector.default_prompt.partial(**mapped_kwargs)
        conditionals = [
            (condition, prompt.partial(**mapped_kwargs))
            for condition, prompt in self.selector.conditionals
        ]
        lc_selector = LangchainSelector(
            default_prompt=default_prompt, conditionals=conditionals
        )

        # copy full prompt object, replace selector
        lc_prompt = deepcopy(self)
        lc_prompt.selector = lc_selector
        return lc_prompt

    def format(self, llm: Optional[BaseLLM] = None, **kwargs: Any) -> str:
        """Format the prompt into a string."""
        from llama_index.llms.langchain import LangChainLLM

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        # if there's mappings specified, make sure those are used
        mapped_kwargs = self._map_all_vars(kwargs)
        return lc_template.format(**mapped_kwargs)

    def format_messages(
        self, llm: Optional[BaseLLM] = None, **kwargs: Any
    ) -> List[ChatMessage]:
        """Format the prompt into a list of chat messages."""
        from llama_index.llms.langchain import LangChainLLM
        from llama_index.llms.langchain_utils import from_lc_messages

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        # if there's mappings specified, make sure those are used
        mapped_kwargs = self._map_all_vars(kwargs)
        lc_prompt_value = lc_template.format_prompt(**mapped_kwargs)
        lc_messages = lc_prompt_value.to_messages()
        return from_lc_messages(lc_messages)

    def get_template(self, llm: Optional[BaseLLM] = None) -> str:
        from llama_index.llms.langchain import LangChainLLM

        if llm is not None:
            # if llamaindex LLM is provided, and we require a langchain LLM,
            # then error. but otherwise if `requires_langchain_llm` is False,
            # then we can just use the default prompt
            if not isinstance(llm, LangChainLLM) and self.requires_langchain_llm:
                raise ValueError("Must provide a LangChainLLM.")
            elif not isinstance(llm, LangChainLLM):
                lc_template = self.selector.default_prompt
            else:
                lc_template = self.selector.get_prompt(llm=llm.llm)
        else:
            lc_template = self.selector.default_prompt

        try:
            return str(lc_template.template)  # type: ignore
        except AttributeError:
            return str(lc_template)
