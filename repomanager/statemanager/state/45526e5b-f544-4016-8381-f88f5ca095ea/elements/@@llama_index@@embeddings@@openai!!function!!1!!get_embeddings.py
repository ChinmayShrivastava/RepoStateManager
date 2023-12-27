def get_embeddings(
    client: OpenAI, list_of_text: List[str], engine: str, **kwargs: Any
) -> List[List[float]]:
    """Get embeddings.

    NOTE: Copied from OpenAI's embedding utils:
    https://github.com/openai/openai-python/blob/main/openai/embeddings_utils.py

    Copied here to avoid importing unnecessary dependencies
    like matplotlib, plotly, scipy, sklearn.

    """
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    data = client.embeddings.create(input=list_of_text, model=engine, **kwargs).data
    return [d.embedding for d in data]
