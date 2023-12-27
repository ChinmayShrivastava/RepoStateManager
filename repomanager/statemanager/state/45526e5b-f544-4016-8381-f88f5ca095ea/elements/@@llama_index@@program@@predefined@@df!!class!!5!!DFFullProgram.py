class DFFullProgram(BasePydanticProgram[DataFrame]):
    """Data-frame program.

    Extracts text into a schema + datapoints.

    """

    def __init__(
        self,
        pydantic_program_cls: Type[BaseLLMFunctionProgram],
        df_parser_template_str: str = DEFAULT_FULL_DF_PARSER_TMPL,
        input_key: str = "input_str",
        **program_kwargs: Any,
    ) -> None:
        """Init params."""
        pydantic_program = pydantic_program_cls.from_defaults(
            DataFrame, df_parser_template_str, **program_kwargs
        )
        self._validate_program(pydantic_program)
        self._pydantic_program = pydantic_program
        self._input_key = input_key

    @classmethod
    def from_defaults(
        cls,
        pydantic_program_cls: Optional[Type[BaseLLMFunctionProgram]] = None,
        df_parser_template_str: str = DEFAULT_FULL_DF_PARSER_TMPL,
        input_key: str = "input_str",
    ) -> "DFFullProgram":
        """Full DF output parser."""
        pydantic_program_cls = pydantic_program_cls or OpenAIPydanticProgram

        return cls(
            pydantic_program_cls,
            df_parser_template_str=df_parser_template_str,
            input_key=input_key,
        )

    def _validate_program(self, pydantic_program: BasePydanticProgram) -> None:
        if pydantic_program.output_cls != DataFrame:
            raise ValueError("Output class of pydantic program must be `DataFrame`.")

    @property
    def output_cls(self) -> Type[DataFrame]:
        """Output class."""
        return DataFrame

    def __call__(self, *args: Any, **kwds: Any) -> DataFrame:
        """Call."""
        if self._input_key not in kwds:
            raise ValueError(f"Input key {self._input_key} not found in kwds.")
        result = self._pydantic_program(**{self._input_key: kwds[self._input_key]})
        return cast(DataFrame, result)
