def display_response(
    response: Response,
    source_length: int = 100,
    show_source: bool = False,
    show_metadata: bool = False,
    show_source_metadata: bool = False,
) -> None:
    """Display response for jupyter notebook."""
    if response.response is None:
        response_text = "None"
    else:
        response_text = response.response.strip()

    display(Markdown(f"**`Final Response:`** {response_text}"))
    if show_source:
        for ind, source_node in enumerate(response.source_nodes):
            display(Markdown("---"))
            display(
                Markdown(f"**`Source Node {ind + 1}/{len(response.source_nodes)}`**")
            )
            display_source_node(
                source_node,
                source_length=source_length,
                show_source_metadata=show_source_metadata,
            )
    if show_metadata:
        if response.metadata is not None:
            display_metadata(response.metadata)
