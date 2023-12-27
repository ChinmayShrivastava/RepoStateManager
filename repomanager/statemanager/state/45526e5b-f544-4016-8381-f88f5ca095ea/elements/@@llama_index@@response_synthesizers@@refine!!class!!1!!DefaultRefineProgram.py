class DefaultRefineProgram(BasePydanticProgram):
    """
    Runs the query on the LLM as normal and always returns the answer with
    query_satisfied=True. In effect, doesn't do any answer filtering.
    """

    def __init__(
        self, prompt: BasePromptTemplate, llm: LLMPredictorType, output_cls: BaseModel
    ):
        self._prompt = prompt
        self._llm = llm
        self._output_cls = output_cls

    @property
    def output_cls(self) -> Type[BaseModel]:
        return StructuredRefineResponse

    def __call__(self, *args: Any, **kwds: Any) -> StructuredRefineResponse:
        if self._output_cls is not None:
            answer = self._llm.structured_predict(
                self._output_cls,
                self._prompt,
                **kwds,
            )
            answer = answer.json()
        else:
            answer = self._llm.predict(
                self._prompt,
                **kwds,
            )
        return StructuredRefineResponse(answer=answer, query_satisfied=True)

    async def acall(self, *args: Any, **kwds: Any) -> StructuredRefineResponse:
        if self._output_cls is not None:
            answer = await self._llm.astructured_predict(
                self._output_cls,
                self._prompt,
                **kwds,
            )
            answer = answer.json()
        else:
            answer = await self._llm.apredict(
                self._prompt,
                **kwds,
            )
        return StructuredRefineResponse(answer=answer, query_satisfied=True)
