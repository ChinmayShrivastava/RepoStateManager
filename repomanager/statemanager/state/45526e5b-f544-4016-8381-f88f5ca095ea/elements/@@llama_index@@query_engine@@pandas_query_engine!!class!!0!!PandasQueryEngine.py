class PandasQueryEngine(BaseQueryEngine):
    """GPT Pandas query.

    Convert natural language to Pandas python code.

    WARNING: This tool provides the Agent access to the `eval` function.
    Arbitrary code execution is possible on the machine running this tool.
    This tool is not recommended to be used in a production setting, and would
    require heavy sandboxing or virtual machines


    Args:
        df (pd.DataFrame): Pandas dataframe to use.
        instruction_str (Optional[str]): Instruction string to use.
        output_processor (Optional[Callable[[str], str]]): Output processor.
            A callable that takes in the output string, pandas DataFrame,
            and any output kwargs and returns a string.
            eg.kwargs["max_colwidth"] = [int] is used to set the length of text
            that each column can display during str(df). Set it to a higher number
            if there is possibly long text in the dataframe.
        pandas_prompt (Optional[BasePromptTemplate]): Pandas prompt to use.
        head (int): Number of rows to show in the table context.

    """

    def __init__(
        self,
        df: pd.DataFrame,
        instruction_str: Optional[str] = None,
        output_processor: Optional[Callable] = None,
        pandas_prompt: Optional[BasePromptTemplate] = None,
        output_kwargs: Optional[dict] = None,
        head: int = 5,
        verbose: bool = False,
        service_context: Optional[ServiceContext] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self._df = df

        self._head = head
        self._pandas_prompt = pandas_prompt or DEFAULT_PANDAS_PROMPT
        self._instruction_str = instruction_str or DEFAULT_INSTRUCTION_STR
        self._output_processor = output_processor or default_output_processor
        self._output_kwargs = output_kwargs or {}
        self._verbose = verbose
        self._service_context = service_context or ServiceContext.from_defaults()

        super().__init__(self._service_context.callback_manager)

    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt sub-modules."""
        return {"pandas_prompt": self._pandas_prompt}

    @classmethod
    def from_index(cls, index: PandasIndex, **kwargs: Any) -> "PandasQueryEngine":
        logger.warning(
            "PandasIndex is deprecated. "
            "Directly construct PandasQueryEngine with df instead."
        )
        return cls(df=index.df, service_context=index.service_context, **kwargs)

    def _get_table_context(self) -> str:
        """Get table context."""
        return str(self._df.head(self._head))

    def _query(self, query_bundle: QueryBundle) -> Response:
        """Answer a query."""
        context = self._get_table_context()

        pandas_response_str = self._service_context.llm.predict(
            self._pandas_prompt,
            df_str=context,
            query_str=query_bundle.query_str,
            instruction_str=self._instruction_str,
        )

        if self._verbose:
            print_text(f"> Pandas Instructions:\n" f"```\n{pandas_response_str}\n```\n")
        pandas_output = self._output_processor(
            pandas_response_str,
            self._df,
            **self._output_kwargs,
        )
        if self._verbose:
            print_text(f"> Pandas Output: {pandas_output}\n")

        response_metadata = {
            "pandas_instruction_str": pandas_response_str,
        }

        return Response(response=pandas_output, metadata=response_metadata)

    async def _aquery(self, query_bundle: QueryBundle) -> Response:
        return self._query(query_bundle)
