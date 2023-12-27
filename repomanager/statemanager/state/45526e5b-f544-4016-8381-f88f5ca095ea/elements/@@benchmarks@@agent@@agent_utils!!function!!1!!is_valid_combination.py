def is_valid_combination(agent: str, model: str) -> bool:
    if agent == "openai" and model not in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
        print(f"{agent} does not work with {model}")
        return False
    return True
