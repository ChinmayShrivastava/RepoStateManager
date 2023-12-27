    def program_factory(*args: Any, **kwargs: Any) -> MockRefineProgram:
        return MockRefineProgram(input_to_query_satisfied)
