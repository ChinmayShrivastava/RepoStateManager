def _mock_conversation(prompt_args: Dict) -> str:
    return prompt_args["history"] + ":" + prompt_args["message"]
