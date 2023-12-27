def mock_extract_triplets(text: str) -> List[Tuple[str, str, str]]:
    """Mock extract triplets."""
    lines = text.split("\n")
    triplets: List[Tuple[str, str, str]] = []
    for line in lines:
        tokens = line[1:-1].split(",")
        tokens = [t.strip() for t in tokens]

        subj, pred, obj = tokens
        triplets.append((subj, pred, obj))
    return triplets
