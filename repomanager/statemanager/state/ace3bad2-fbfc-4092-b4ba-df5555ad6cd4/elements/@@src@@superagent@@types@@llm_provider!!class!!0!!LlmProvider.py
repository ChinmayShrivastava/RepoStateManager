class LlmProvider(str, enum.Enum):
    """
    An enumeration.
    """

    OPENAI = "OPENAI"
    AZURE_OPENAI = "AZURE_OPENAI"
    HUGGINGFACE = "HUGGINGFACE"

    def visit(
        self,
        openai: typing.Callable[[], T_Result],
        azure_openai: typing.Callable[[], T_Result],
        huggingface: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is LlmProvider.OPENAI:
            return openai()
        if self is LlmProvider.AZURE_OPENAI:
            return azure_openai()
        if self is LlmProvider.HUGGINGFACE:
            return huggingface()
