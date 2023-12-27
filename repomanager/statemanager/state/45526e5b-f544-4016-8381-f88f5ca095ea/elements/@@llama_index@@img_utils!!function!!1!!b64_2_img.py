def b64_2_img(data: str) -> Image:
    """Convert base64 encoded image str to a PIL.Image."""
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)
