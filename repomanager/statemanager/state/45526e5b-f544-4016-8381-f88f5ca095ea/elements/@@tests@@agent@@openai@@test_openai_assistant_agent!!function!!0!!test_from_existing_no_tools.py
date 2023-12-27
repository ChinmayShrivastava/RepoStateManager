def test_from_existing_no_tools() -> None:
    assistant_id = "test-id"
    api_key = "test-api-key"
    mock_assistant = MagicMock()

    with patch.object(openai, "OpenAI") as mock_openai:
        mock_openai.return_value.beta.assistants.retrieve.return_value = mock_assistant
        agent = OpenAIAssistantAgent.from_existing(
            assistant_id=assistant_id,
            thread_id="your_thread_id",
            instructions_prefix="your_instructions_prefix",
            run_retrieve_sleep_time=0,
            api_key=api_key,
        )

    mock_openai.assert_called_once_with(api_key=api_key)
    mock_openai.return_value.beta.assistants.retrieve.assert_called_once_with(
        assistant_id
    )
    assert isinstance(agent, OpenAIAssistantAgent)
