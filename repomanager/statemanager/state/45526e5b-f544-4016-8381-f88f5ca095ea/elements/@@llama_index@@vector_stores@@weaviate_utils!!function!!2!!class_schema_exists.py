def class_schema_exists(client: Any, class_name: str) -> bool:
    """Check if class schema exists."""
    validate_client(client)
    schema = client.schema.get()
    classes = schema["classes"]
    existing_class_names = {c["class"] for c in classes}
    return class_name in existing_class_names
