class GPTIndexMemory(Memory):
    """Langchain memory wrapper (for LlamaIndex).

    Args:
        human_prefix (str): Prefix for human input. Defaults to "Human".
        ai_prefix (str): Prefix for AI output. Defaults to "AI".
        memory_key (str): Key for memory. Defaults to "history".
        index (BaseIndex): LlamaIndex instance.
        query_kwargs (Dict[str, Any]): Keyword arguments for LlamaIndex query.
        input_key (Optional[str]): Input key. Defaults to None.
        output_key (Optional[str]): Output key. Defaults to None.

    """

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"
    index: BaseIndex
    query_kwargs: Dict = Field(default_factory=dict)
    output_key: Optional[str] = None
    input_key: Optional[str] = None

    @property
    def memory_variables(self) -> List[str]:
        """Return memory variables."""
        return [self.memory_key]

    def _get_prompt_input_key(self, inputs: Dict[str, Any]) -> str:
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        return prompt_input_key

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return key-value pairs given the text input to the chain."""
        prompt_input_key = self._get_prompt_input_key(inputs)
        query_str = inputs[prompt_input_key]

        # TODO: wrap in prompt
        # TODO: add option to return the raw text
        # NOTE: currently it's a hack
        query_engine = self.index.as_query_engine(**self.query_kwargs)
        response = query_engine.query(query_str)
        return {self.memory_key: str(response)}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save the context of this model run to memory."""
        prompt_input_key = self._get_prompt_input_key(inputs)
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = next(iter(outputs.keys()))
        else:
            output_key = self.output_key
        human = f"{self.human_prefix}: " + inputs[prompt_input_key]
        ai = f"{self.ai_prefix}: " + outputs[output_key]
        doc_text = f"{human}\n{ai}"
        doc = Document(text=doc_text)
        self.index.insert(doc)

    def clear(self) -> None:
        """Clear memory contents."""

    def __repr__(self) -> str:
        """Return representation."""
        return "GPTIndexMemory()"
