class DFRowsProgram(BasePydanticProgram[DataFrameRowsOnly]):
    """DF Rows output parser.

    Given DF schema, extract text into a set of rows.

    """

    def __init__(
        self,
        pydantic_program_cls: Type[BaseLLMFunctionProgram],
        df_parser_template_str: str = DEFAULT_ROWS_DF_PARSER_TMPL,
        column_schema: Optional[str] = None,
        input_key: str = "input_str",
        **program_kwargs: Any,
    ) -> None:
        """Init params."""
        # partial format df parser template string with column schema
        prompt_template_str = df_parser_template_str.replace(
            "{column_schema}", column_schema or ""
        )

        pydantic_program = pydantic_program_cls.from_defaults(
            DataFrameRowsOnly, prompt_template_str, **program_kwargs
        )
        self._validate_program(pydantic_program)
        self._pydantic_program = pydantic_program
        self._input_key = input_key

    def _validate_program(self, pydantic_program: BasePydanticProgram) -> None:
        if pydantic_program.output_cls != DataFrameRowsOnly:
            raise ValueError(
                "Output class of pydantic program must be `DataFramRowsOnly`."
            )

    @classmethod
    def from_defaults(
        cls,
        pydantic_program_cls: Optional[Type[BaseLLMFunctionProgram]] = None,
        df_parser_template_str: str = DEFAULT_ROWS_DF_PARSER_TMPL,
        df: Optional[pd.DataFrame] = None,
        column_schema: Optional[str] = None,
        input_key: str = "input_str",
        **kwargs: Any,
    ) -> "DFRowsProgram":
        """Rows DF output parser."""
        pydantic_program_cls = pydantic_program_cls or OpenAIPydanticProgram

        # either one of df or column_schema needs to be specified
        if df is None and column_schema is None:
            raise ValueError(
                "Either `df` or `column_schema` must be specified for "
                "DFRowsOutputParser."
            )
        # first, inject the column schema into the template string
        if column_schema is None:
            assert df is not None
            # by default, show column schema and some example values
            column_schema = ", ".join(df.columns)

        return cls(
            pydantic_program_cls,
            df_parser_template_str=df_parser_template_str,
            column_schema=column_schema,
            input_key=input_key,
            **kwargs,
        )

    @property
    def output_cls(self) -> Type[DataFrameRowsOnly]:
        """Output class."""
        return DataFrameRowsOnly

    def __call__(self, *args: Any, **kwds: Any) -> DataFrameRowsOnly:
        """Call."""
        if self._input_key not in kwds:
            raise ValueError(f"Input key {self._input_key} not found in kwds.")
        result = self._pydantic_program(**{self._input_key: kwds[self._input_key]})
        return cast(DataFrameRowsOnly, result)
