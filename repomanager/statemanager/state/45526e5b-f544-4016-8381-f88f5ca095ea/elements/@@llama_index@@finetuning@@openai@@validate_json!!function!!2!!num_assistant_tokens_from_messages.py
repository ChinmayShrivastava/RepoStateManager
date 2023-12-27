    def num_assistant_tokens_from_messages(messages: List[dict]) -> int:
        num_tokens = 0
        for message in messages:
            if message["role"] == "assistant":
                num_tokens += len(encoding.encode(message["content"]))
        return num_tokens
