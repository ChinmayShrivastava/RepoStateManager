class MockRefineProgram(BasePydanticProgram):
    """
    Runs the query on the LLM as normal and always returns the answer with
    query_satisfied=True. In effect, doesn't do any answer filtering.
    """

    def __init__(self, input_to_query_satisfied: Dict[str, bool]):
        self._input_to_query_satisfied = input_to_query_satisfied

    @property
    def output_cls(self) -> Type[BaseModel]:
        return StructuredRefineResponse

    def __call__(
        self,
        *args: Any,
        context_str: Optional[str] = None,
        context_msg: Optional[str] = None,
        **kwargs: Any
    ) -> StructuredRefineResponse:
        input_str = context_str or context_msg
        input_str = cast(str, input_str)
        query_satisfied = self._input_to_query_satisfied[input_str]
        return StructuredRefineResponse(
            answer=input_str, query_satisfied=query_satisfied
        )

    async def acall(
        self,
        *args: Any,
        context_str: Optional[str] = None,
        context_msg: Optional[str] = None,
        **kwargs: Any
    ) -> StructuredRefineResponse:
        input_str = context_str or context_msg
        input_str = cast(str, input_str)
        query_satisfied = self._input_to_query_satisfied[input_str]
        return StructuredRefineResponse(
            answer=input_str, query_satisfied=query_satisfied
        )
