def set_global_handler(eval_mode: str, **eval_params: Any) -> None:
    """Set global eval handlers."""
    import llama_index

    llama_index.global_handler = create_global_handler(eval_mode, **eval_params)
