class RetrievalEvalMode(str, Enum):
    """Evaluation of retrieval modality."""

    TEXT = "text"
    IMAGE = "image"

    @classmethod
    def from_str(cls, label: str) -> "RetrievalEvalMode":
        if label == "text":
            return RetrievalEvalMode.TEXT
        elif label == "image":
            return RetrievalEvalMode.IMAGE
        else:
            raise NotImplementedError
