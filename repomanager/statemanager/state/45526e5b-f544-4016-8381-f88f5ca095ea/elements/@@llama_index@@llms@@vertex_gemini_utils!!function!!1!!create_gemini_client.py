def create_gemini_client(model: str) -> Any:
    from vertexai.preview.generative_models import GenerativeModel

    return GenerativeModel(model_name=model)
