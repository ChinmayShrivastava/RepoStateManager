class GradientModel(MagicMock):
    """MockGradientModel."""

    def complete(self, query: str, max_generated_token_count: int) -> Any:
        """Just duplicate the query m times."""
        output = MagicMock()
        output.generated_output = f"{query*max_generated_token_count}"
        return output

    async def acomplete(self, query: str, max_generated_token_count: int) -> Any:
        """Just duplicate the query m times."""
        output = MagicMock()
        output.generated_output = f"{query*max_generated_token_count}"
        return output
