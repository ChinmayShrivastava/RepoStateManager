class ImageDocument(Document, ImageNode):
    """Data document containing an image."""

    @classmethod
    def class_name(cls) -> str:
        return "ImageDocument"
