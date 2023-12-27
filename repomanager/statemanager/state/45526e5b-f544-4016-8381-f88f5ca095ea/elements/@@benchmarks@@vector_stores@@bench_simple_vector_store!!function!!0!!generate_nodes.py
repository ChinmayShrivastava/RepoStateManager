def generate_nodes(
    num_vectors: int = 100, embedding_length: int = 1536
) -> List[TextNode]:
    random.seed(42)  # Make this reproducible
    return [
        TextNode(
            embedding=[random.uniform(0, 1) for _ in range(embedding_length)],
        )
        for _ in range(num_vectors)
    ]
