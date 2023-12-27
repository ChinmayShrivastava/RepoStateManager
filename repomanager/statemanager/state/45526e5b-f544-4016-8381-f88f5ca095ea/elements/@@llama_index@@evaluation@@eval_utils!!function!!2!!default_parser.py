def default_parser(eval_response: str) -> Tuple[float, str]:
    """
    Default parser function for evaluation response.

    Args:
        eval_response (str): The response string from the evaluation.

    Returns:
        Tuple[float, str]: A tuple containing the score as a float and the reasoning as a string.
    """
    score_str, reasoning_str = eval_response.split("\n", 1)
    score = float(score_str)
    reasoning = reasoning_str.lstrip("\n")
    return score, reasoning
