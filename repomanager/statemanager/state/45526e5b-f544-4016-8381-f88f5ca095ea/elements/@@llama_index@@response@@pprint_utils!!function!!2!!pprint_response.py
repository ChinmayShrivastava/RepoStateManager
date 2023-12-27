def pprint_response(
    response: Response,
    source_length: int = 350,
    wrap_width: int = 70,
    show_source: bool = False,
) -> None:
    """Pretty print response for jupyter notebook."""
    if response.response is None:
        response_text = "None"
    else:
        response_text = response.response.strip()

    response_text = f"Final Response: {response_text}"
    print(textwrap.fill(response_text, width=wrap_width))

    if show_source:
        for ind, source_node in enumerate(response.source_nodes):
            print("_" * wrap_width)
            print(f"Source Node {ind + 1}/{len(response.source_nodes)}")
            pprint_source_node(
                source_node, source_length=source_length, wrap_width=wrap_width
            )
