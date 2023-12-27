class EvaluationSource(str, Enum):
    """To distinguish between flipped or original."""

    ORIGINAL = "original"
    FLIPPED = "flipped"
    NEITHER = "neither"
