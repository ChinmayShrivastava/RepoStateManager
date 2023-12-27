class NoSuchCorpusException(Exception):
    def __init__(self, *, corpus_id: str) -> None:
        super().__init__(f"No such corpus {corpus_id} found")
