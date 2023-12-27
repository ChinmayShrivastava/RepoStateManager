def get_embedding(client: OpenAI, text: str, engine: str, **kwargs: Any) -> List[float]:
    """Get embedding.

    NOTE: Copied from OpenAI's embedding utils:
    https://github.com/openai/openai-python/blob/main/openai/embeddings_utils.py

    Copied here to avoid importing unnecessary dependencies
    like matplotlib, plotly, scipy, sklearn.

    """
    text = text.replace("\n", " ")

    return (
        client.embeddings.create(input=[text], model=engine, **kwargs).data[0].embedding
    )
