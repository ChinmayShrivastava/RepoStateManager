def json_schema_to_guidance_output_template(
    schema: dict,
    key: Optional[str] = None,
    indent: int = 0,
    root: Optional[dict] = None,
    use_pattern_control: bool = False,
) -> str:
    """Convert a json schema to guidance output template.

    Implementation based on https://github.com/microsoft/guidance/\
        blob/main/notebooks/applications/jsonformer.ipynb
    Modified to support nested pydantic models.
    """
    out = ""
    if "type" not in schema and "$ref" in schema:
        if root is None:
            raise ValueError("Must specify root schema for nested object")

        ref = schema["$ref"]
        model = ref.split("/")[-1]
        return json_schema_to_guidance_output_template(
            root["definitions"][model], key, indent, root
        )

    if schema["type"] == "object":
        out += "  " * indent + "{\n"
        for k, v in schema["properties"].items():
            out += (
                "  " * (indent + 1)
                + f'"{k}"'
                + ": "
                + json_schema_to_guidance_output_template(v, k, indent + 1, root)
                + ",\n"
            )
        out += "  " * indent + "}"
        return out
    elif schema["type"] == "array":
        if key is None:
            raise ValueError("Key should not be None")
        if "max_items" in schema:
            extra_args = f" max_iterations={schema['max_items']}"
        else:
            extra_args = ""
        return (
            "[{{#geneach '"
            + key
            + "' stop=']'"
            + extra_args
            + "}}{{#unless @first}}, {{/unless}}"
            + json_schema_to_guidance_output_template(schema["items"], "this", 0, root)
            + "{{/geneach}}]"
        )
    elif schema["type"] == "string":
        if key is None:
            raise ValueError("key should not be None")
        return "\"{{gen '" + key + "' stop='\"'}}\""
    elif schema["type"] in ["integer", "number"]:
        if key is None:
            raise ValueError("key should not be None")
        if use_pattern_control:
            return "{{gen '" + key + "' pattern='[0-9\\.]' stop=','}}"
        else:
            return "\"{{gen '" + key + "' stop='\"'}}\""
    elif schema["type"] == "boolean":
        if key is None:
            raise ValueError("key should not be None")
        return "{{#select '" + key + "'}}True{{or}}False{{/select}}"
    else:
        schema_type = schema["type"]
        raise ValueError(f"Unknown schema type {schema_type}")
