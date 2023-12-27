class Corpus:
    name: str
    display_name: Optional[str]
    create_time: Optional[timestamp_pb2.Timestamp]
    update_time: Optional[timestamp_pb2.Timestamp]

    @property
    def corpus_id(self) -> str:
        name = EntityName.from_str(self.name)
        return name.corpus_id

    @classmethod
    def from_corpus(cls, c: genai.Corpus) -> "Corpus":
        return cls(
            name=c.name,
            display_name=c.display_name,
            create_time=c.create_time,
            update_time=c.update_time,
        )
