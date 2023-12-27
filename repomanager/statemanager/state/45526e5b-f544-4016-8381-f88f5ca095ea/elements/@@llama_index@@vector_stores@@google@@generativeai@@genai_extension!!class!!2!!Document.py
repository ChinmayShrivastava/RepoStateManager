class Document:
    name: str
    display_name: Optional[str]
    create_time: Optional[timestamp_pb2.Timestamp]
    update_time: Optional[timestamp_pb2.Timestamp]
    custom_metadata: Optional[MutableSequence[genai.CustomMetadata]]

    @property
    def corpus_id(self) -> str:
        name = EntityName.from_str(self.name)
        return name.corpus_id

    @property
    def document_id(self) -> str:
        name = EntityName.from_str(self.name)
        assert isinstance(name.document_id, str)
        return name.document_id

    @classmethod
    def from_document(cls, d: genai.Document) -> "Document":
        return cls(
            name=d.name,
            display_name=d.display_name,
            create_time=d.create_time,
            update_time=d.update_time,
            custom_metadata=d.custom_metadata,
        )
