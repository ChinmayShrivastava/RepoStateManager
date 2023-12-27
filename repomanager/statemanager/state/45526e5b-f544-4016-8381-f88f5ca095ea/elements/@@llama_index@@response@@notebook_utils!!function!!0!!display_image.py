def display_image(img_str: str, size: Tuple[int, int] = DEFAULT_THUMBNAIL_SIZE) -> None:
    """Display base64 encoded image str as image for jupyter notebook."""
    img = b64_2_img(img_str)
    img.thumbnail(size)
    display(img)
