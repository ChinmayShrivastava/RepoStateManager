class EntityName:
    corpus_id: str
    document_id: Optional[str] = None
    chunk_id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.chunk_id is not None and self.document_id is None:
            raise ValueError(f"Chunk must have document ID but found {self}")

    @classmethod
    def from_str(cls, encoded: str) -> "EntityName":
        matched = _NAME_REGEX.match(encoded)
        if not matched:
            raise ValueError(f"Invalid entity name: {encoded}")

        return cls(
            corpus_id=matched.group(1),
            document_id=matched.group(3),
            chunk_id=matched.group(5),
        )

    def __repr__(self) -> str:
        name = f"corpora/{self.corpus_id}"
        if self.document_id is None:
            return name
        name += f"/documents/{self.document_id}"
        if self.chunk_id is None:
            return name
        name += f"/chunks/{self.chunk_id}"
        return name

    def __str__(self) -> str:
        return repr(self)

    def is_corpus(self) -> bool:
        return self.document_id is None

    def is_document(self) -> bool:
        return self.document_id is not None and self.chunk_id is None

    def is_chunk(self) -> bool:
        return self.chunk_id is not None
