class MockXinferenceModel:
    def chat(
        self,
        prompt: str,
        chat_history: List[Mapping[str, Any]],
        generate_config: Dict[str, Any],
    ) -> Union[Iterator[Dict[str, Any]], Dict[str, Any]]:
        assert isinstance(prompt, str)
        if chat_history is not None:
            for chat_item in chat_history:
                assert "role" in chat_item
                assert isinstance(chat_item["role"], str)
                assert "content" in chat_item
                assert isinstance(chat_item["content"], str)

        if "stream" in generate_config and generate_config["stream"] is True:
            return mock_chat_stream_iterator()
        else:
            return mock_chat
