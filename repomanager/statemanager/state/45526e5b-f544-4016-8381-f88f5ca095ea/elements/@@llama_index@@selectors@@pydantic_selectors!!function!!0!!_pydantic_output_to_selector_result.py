def _pydantic_output_to_selector_result(output: Any) -> SelectorResult:
    """
    Convert pydantic output to selector result.
    Takes into account zero-indexing on answer indexes.
    """
    if isinstance(output, SingleSelection):
        output.index -= 1
        return SelectorResult(selections=[output])
    elif isinstance(output, MultiSelection):
        for idx in range(len(output.selections)):
            output.selections[idx].index -= 1
        return SelectorResult(selections=output.selections)
    else:
        raise ValueError(f"Unsupported output type: {type(output)}")
