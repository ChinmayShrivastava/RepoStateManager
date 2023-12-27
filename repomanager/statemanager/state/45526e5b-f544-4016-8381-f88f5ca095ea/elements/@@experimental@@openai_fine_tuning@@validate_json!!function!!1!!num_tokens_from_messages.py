    def num_tokens_from_messages(
        messages: List[dict], tokens_per_message: int = 3, tokens_per_name: int = 1
    ) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3
        return num_tokens
