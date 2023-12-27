    def test_output_processor(llm_output: str, json_value: JSONType) -> JSONType:
        assert llm_output == TEST_LLM_OUTPUT
        assert json_value == json_val
        return [test_json_return_value]
