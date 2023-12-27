def format_query(
    query: str, model_name: Optional[str], instruction: Optional[str] = None
) -> str:
    if instruction is None:
        instruction = get_query_instruct_for_model_name(model_name)
    # NOTE: strip() enables backdoor for defeating instruction prepend by
    # passing empty string
    return f"{instruction} {query}".strip()
