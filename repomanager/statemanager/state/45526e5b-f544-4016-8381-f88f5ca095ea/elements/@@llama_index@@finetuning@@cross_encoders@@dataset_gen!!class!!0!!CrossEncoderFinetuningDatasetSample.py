class CrossEncoderFinetuningDatasetSample:
    """Class for keeping track of each item of Cross-Encoder training Dataset."""

    query: str
    context: str
    score: int
