    def _convert_gemini_part_to_prompt(part: Union[str, Dict]) -> Part:
        from vertexai.preview.generative_models import Image, Part

        if isinstance(part, str):
            return Part.from_text(part)

        if not isinstance(part, Dict):
            raise ValueError(
                f"Message's content is expected to be a dict, got {type(part)}!"
            )
        if part["type"] == "text":
            return Part.from_text(part["text"])
        elif part["type"] == "image_url":
            path = part["image_url"]
            if path.startswith("gs://"):
                raise ValueError("Only local image path is supported!")
            elif path.startswith("data:image/jpeg;base64,"):
                image = Image.from_bytes(base64.b64decode(path[23:]))
            else:
                image = Image.load_from_file(path)
        else:
            raise ValueError("Only text and image_url types are supported!")
        return Part.from_image(image)
