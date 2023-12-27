def display_image_uris(
    image_paths: List[str],
    image_matrix: Tuple[int, int] = DEFAULT_IMAGE_MATRIX,
    top_k: int = DEFAULT_SHOW_TOP_K,
) -> None:
    """Display base64 encoded image str as image for jupyter notebook."""
    images_shown = 0
    plt.figure(figsize=(16, 9))
    for img_path in image_paths[:top_k]:
        if os.path.isfile(img_path):
            image = Image.open(img_path)

            plt.subplot(image_matrix[0], image_matrix[1], images_shown + 1)
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])

            images_shown += 1
            if images_shown >= image_matrix[0] * image_matrix[1]:
                break
