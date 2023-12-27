def get_all_properties(client: Any, class_name: str) -> List[str]:
    """Get all properties of a class."""
    validate_client(client)
    schema = client.schema.get()
    classes = schema["classes"]
    classes_by_name = {c["class"]: c for c in classes}
    if class_name not in classes_by_name:
        raise ValueError(f"{class_name} schema does not exist.")
    schema = classes_by_name[class_name]
    return [p["name"] for p in schema["properties"]]
