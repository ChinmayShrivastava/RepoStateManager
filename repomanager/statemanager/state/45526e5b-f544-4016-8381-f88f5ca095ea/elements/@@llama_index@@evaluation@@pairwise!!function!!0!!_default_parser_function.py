def _default_parser_function(
    eval_response: str,
) -> Tuple[Optional[bool], Optional[float], Optional[str]]:
    # Extract from response
    feedback: Optional[str] = ""
    if "[[A]]" in eval_response:
        passing: Optional[bool] = True
        score = 1.0
    elif "[[B]]" in eval_response:
        passing = False
        score = 0.0
    elif "[[C]]" in eval_response:
        passing = None
        score = 0.5
    else:
        passing = None
        score = None
        feedback = None
    return passing, score, feedback
