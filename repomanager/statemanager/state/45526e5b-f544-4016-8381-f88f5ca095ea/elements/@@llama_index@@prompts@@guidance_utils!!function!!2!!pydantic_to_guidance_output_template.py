def pydantic_to_guidance_output_template(cls: Type[BaseModel]) -> str:
    """Convert a pydantic model to guidance output template."""
    return json_schema_to_guidance_output_template(cls.schema(), root=cls.schema())
