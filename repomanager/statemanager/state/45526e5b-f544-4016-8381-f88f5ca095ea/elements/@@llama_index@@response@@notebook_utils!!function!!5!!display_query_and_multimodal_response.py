def display_query_and_multimodal_response(
    query_str: str, response: Response, plot_height: int = 2, plot_width: int = 5
) -> None:
    """For displaying a query and its multi-modal response."""
    if response.metadata:
        image_nodes = response.metadata["image_nodes"] or []
    else:
        image_nodes = []
    num_subplots = len(image_nodes)

    f, axarr = plt.subplots(1, num_subplots)
    f.set_figheight(plot_height)
    f.set_figwidth(plot_width)
    ix = 0
    for ix, scored_img_node in enumerate(image_nodes):
        img_node = scored_img_node.node
        image = None
        if img_node.image_url:
            img_response = requests.get(img_node.image_url)
            image = Image.open(BytesIO(img_response.content))
        elif img_node.image_path:
            image = Image.open(img_node.image_path).convert("RGB")
        else:
            raise ValueError(
                "A retrieved image must have image_path or image_url specified."
            )
        if num_subplots > 1:
            axarr[ix].imshow(image)
            axarr[ix].set_title(f"Retrieved Position: {ix}", pad=10, fontsize=9)
        else:
            axarr.imshow(image)
            axarr.set_title(f"Retrieved Position: {ix}", pad=10, fontsize=9)

    f.tight_layout()
    print(f"Query: {query_str}\n=======")
    print(f"Retrieved Images:\n")
    plt.show()
    print("=======")
    print(f"Response: {response.response}\n=======\n")
