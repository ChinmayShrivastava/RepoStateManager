def mock_extract_kg_triplets_response(
    text_chunk: str, max_triplets: Optional[int] = None
) -> str:
    """Generate 1 or more fake triplets."""
    response = ""
    if max_triplets is not None:
        for i in range(max_triplets):
            response += "(This is, a mock, triplet)\n"
    else:
        response += "(This is, a mock, triplet)\n"

    return response
