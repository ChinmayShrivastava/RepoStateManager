def call_function(
    tools: List[BaseTool], fn_obj: Any, verbose: bool = False
) -> Tuple[ChatMessage, ToolOutput]:
    """Call a function and return the output as a string."""
    from openai.types.beta.threads.required_action_function_tool_call import Function

    fn_obj = cast(Function, fn_obj)
    # TMP: consolidate with other abstractions
    name = fn_obj.name
    arguments_str = fn_obj.arguments
    if verbose:
        print("=== Calling Function ===")
        print(f"Calling function: {name} with args: {arguments_str}")
    tool = get_function_by_name(tools, name)
    argument_dict = json.loads(arguments_str)
    output = tool(**argument_dict)
    if verbose:
        print(f"Got output: {output!s}")
        print("========================")
    return (
        ChatMessage(
            content=str(output),
            role=MessageRole.FUNCTION,
            additional_kwargs={
                "name": fn_obj.name,
            },
        ),
        output,
    )
