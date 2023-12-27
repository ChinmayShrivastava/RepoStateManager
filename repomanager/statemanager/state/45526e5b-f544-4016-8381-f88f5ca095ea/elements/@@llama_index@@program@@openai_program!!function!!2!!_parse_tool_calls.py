def _parse_tool_calls(
    tool_calls: List[OpenAIToolCall],
    output_cls: Type[Model],
    allow_multiple: bool = False,
    verbose: bool = False,
) -> Union[Model, List[Model]]:
    outputs = []
    for tool_call in tool_calls:
        function_call = tool_call.function
        # validations to get passed mypy
        assert function_call is not None
        assert function_call.name is not None
        assert function_call.arguments is not None
        if verbose:
            name = function_call.name
            arguments_str = function_call.arguments
            print(f"Function call: {name} with args: {arguments_str}")

        if isinstance(function_call.arguments, dict):
            output = output_cls.parse_obj(function_call.arguments)
        else:
            output = output_cls.parse_raw(function_call.arguments)

        outputs.append(output)

    if allow_multiple:
        return outputs
    else:
        if len(outputs) > 1:
            _logger.warning(
                "Multiple outputs found, returning first one. "
                "If you want to return all outputs, set output_multiple=True."
            )

        return outputs[0]
