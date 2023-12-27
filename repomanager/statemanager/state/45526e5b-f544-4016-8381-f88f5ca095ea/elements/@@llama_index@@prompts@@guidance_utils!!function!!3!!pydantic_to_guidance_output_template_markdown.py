def pydantic_to_guidance_output_template_markdown(cls: Type[BaseModel]) -> str:
    """Convert a pydantic model to guidance output template wrapped in json markdown."""
    output = json_schema_to_guidance_output_template(cls.schema(), root=cls.schema())
    return wrap_json_markdown(output)
