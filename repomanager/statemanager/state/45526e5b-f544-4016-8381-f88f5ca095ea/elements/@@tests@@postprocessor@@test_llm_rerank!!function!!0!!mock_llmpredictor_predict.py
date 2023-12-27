def mock_llmpredictor_predict(
    self: Any, prompt: BasePromptTemplate, **prompt_args: Any
) -> str:
    """Patch llm predictor predict."""
    context_str = prompt_args["context_str"]
    node_strs = context_str.split("\n")
    node_to_choice_and_score = {
        "Test": (True, "1"),
        "Test2": (False, "0"),
        "Test3": (True, "3"),
        "Test4": (False, "0"),
        "Test5": (True, "5"),
        "Test6": (False, "0"),
        "Test7": (True, "7"),
        "Test8": (False, "0"),
    }
    choices_and_scores = []
    for idx, node_str in enumerate(node_strs):
        choice, score = node_to_choice_and_score[node_str]
        if choice:
            choices_and_scores.append((idx + 1, score))

    result_strs = [f"Doc: {c!s}, Relevance: {s}" for c, s in choices_and_scores]
    return "\n".join(result_strs)
