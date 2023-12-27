def to_openai_function(pydantic_class: Type[BaseModel]) -> Dict[str, Any]:
    """Deprecated in favor of `to_openai_tool`.

    Convert pydantic class to OpenAI function.
    """
    return to_openai_tool(pydantic_class)
