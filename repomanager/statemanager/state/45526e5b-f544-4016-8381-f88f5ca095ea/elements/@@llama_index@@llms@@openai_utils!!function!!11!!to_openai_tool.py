def to_openai_tool(pydantic_class: Type[BaseModel]) -> Dict[str, Any]:
    """Convert pydantic class to OpenAI tool."""
    schema = pydantic_class.schema()
    function = {
        "name": schema["title"],
        "description": schema["description"],
        "parameters": pydantic_class.schema(),
    }
    return {"type": "function", "function": function}
