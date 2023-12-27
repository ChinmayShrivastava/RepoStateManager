def _mock_knowledge_graph_triplet_extract(prompt_args: Dict, max_triplets: int) -> str:
    """Mock knowledge graph triplet extract."""
    return mock_extract_kg_triplets_response(
        prompt_args["text"], max_triplets=max_triplets
    )
