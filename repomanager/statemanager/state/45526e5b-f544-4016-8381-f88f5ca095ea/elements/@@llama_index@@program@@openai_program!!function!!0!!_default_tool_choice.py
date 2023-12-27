def _default_tool_choice(
    output_cls: Type[Model], allow_multiple: bool = False
) -> Union[str, Dict[str, Any]]:
    """Default OpenAI tool to choose."""
    if allow_multiple:
        return "auto"
    else:
        schema = output_cls.schema()
        return resolve_tool_choice(schema["title"])
