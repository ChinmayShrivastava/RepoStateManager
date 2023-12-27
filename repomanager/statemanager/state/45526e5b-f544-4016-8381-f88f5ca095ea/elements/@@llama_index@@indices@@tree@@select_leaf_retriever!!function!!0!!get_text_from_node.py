def get_text_from_node(
    node: BaseNode,
    level: Optional[int] = None,
    verbose: bool = False,
) -> str:
    """Get text from node."""
    level_str = "" if level is None else f"[Level {level}]"
    fmt_text_chunk = truncate_text(node.get_content(metadata_mode=MetadataMode.LLM), 50)
    logger.debug(f">{level_str} Searching in chunk: {fmt_text_chunk}")

    response_txt = node.get_content(metadata_mode=MetadataMode.LLM)
    fmt_response = truncate_text(response_txt, 200)
    if verbose:
        print_text(f">{level_str} Got node text: {fmt_response}\n", color="blue")
    return response_txt
