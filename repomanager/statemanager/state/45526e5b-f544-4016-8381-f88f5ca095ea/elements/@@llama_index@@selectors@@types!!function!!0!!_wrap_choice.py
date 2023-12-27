def _wrap_choice(choice: MetadataType) -> ToolMetadata:
    if isinstance(choice, ToolMetadata):
        return choice
    elif isinstance(choice, str):
        return ToolMetadata(description=choice)
    else:
        raise ValueError(f"Unexpected type: {type(choice)}")
