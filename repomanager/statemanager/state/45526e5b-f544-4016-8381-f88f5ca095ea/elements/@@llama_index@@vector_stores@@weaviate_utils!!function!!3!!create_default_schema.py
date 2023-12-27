def create_default_schema(client: Any, class_name: str) -> None:
    """Create default schema."""
    validate_client(client)
    class_schema = {
        "class": class_name,
        "description": f"Class for {class_name}",
        "properties": NODE_SCHEMA,
    }
    client.schema.create_class(class_schema)
