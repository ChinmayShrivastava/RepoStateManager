def _extract_chunk_id(entity_name: str) -> str:
    try:
        import llama_index.vector_stores.google.generativeai.genai_extension as genaix
    except ImportError:
        raise ImportError(_import_err_msg)

    id = genaix.EntityName.from_str(entity_name).chunk_id
    assert id is not None
    return id
