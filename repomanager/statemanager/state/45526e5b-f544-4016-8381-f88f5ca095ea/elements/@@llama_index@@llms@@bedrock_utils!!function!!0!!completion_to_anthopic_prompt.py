def completion_to_anthopic_prompt(completion: str) -> str:
    return messages_to_anthropic_prompt(prompt_to_messages(completion))
