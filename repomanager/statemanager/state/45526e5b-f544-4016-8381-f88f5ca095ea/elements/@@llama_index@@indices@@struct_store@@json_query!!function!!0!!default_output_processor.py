def default_output_processor(llm_output: str, json_value: JSONType) -> JSONType:
    """Default output processor that extracts values based on JSON Path expressions."""
    # Split the given string into separate JSON Path expressions
    expressions = [expr.strip() for expr in llm_output.split(",")]

    try:
        from jsonpath_ng.ext import parse
        from jsonpath_ng.jsonpath import DatumInContext
    except ImportError as exc:
        IMPORT_ERROR_MSG = "You need to install jsonpath-ng to use this function!"
        raise ImportError(IMPORT_ERROR_MSG) from exc

    results = {}

    for expression in expressions:
        try:
            datum: List[DatumInContext] = parse(expression).find(json_value)
            if datum:
                key = expression.split(".")[
                    -1
                ]  # Extracting "title" from "$.title", for example
                results[key] = datum[0].value
        except Exception as exc:
            raise ValueError(f"Invalid JSON Path: {expression}") from exc

    return results
