def img_2_b64(image: Image, format: str = "JPEG") -> str:
    """Convert a PIL.Image to a base64 encoded image str."""
    buff = BytesIO()
    image.save(buff, format=format)
    return cast(str, base64.b64encode(buff.getvalue()))
