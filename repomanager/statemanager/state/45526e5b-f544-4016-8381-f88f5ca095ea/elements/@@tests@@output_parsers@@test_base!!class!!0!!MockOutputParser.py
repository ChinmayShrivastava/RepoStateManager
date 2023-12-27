    class MockOutputParser(LCOutputParser):
        """Mock output parser.

        Similar to langchain's StructuredOutputParser, but better for testing.

        """

        response_schema: ResponseSchema

        def get_format_instructions(self) -> str:
            """Get format instructions."""
            return (
                f"{{ {self.response_schema.name}, {self.response_schema.description} }}"
            )

        def parse(self, text: str) -> str:
            """Parse the output of an LLM call."""
            # TODO: make this better
            return text
