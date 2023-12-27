class QueryResponseDataset(BaseModel):
    """Query Response Dataset.

    The response can be empty if the dataset is generated from documents.

    Args:
        queries (Dict[str, str]): Query id -> query.
        responses (Dict[str, str]): Query id -> response.

    """

    queries: Dict[str, str] = Field(
        default_factory=dict, description="Query id -> query"
    )
    responses: Dict[str, str] = Field(
        default_factory=dict, description="Query id -> response"
    )

    @classmethod
    def from_qr_pairs(
        cls,
        qr_pairs: List[Tuple[str, str]],
    ) -> QueryResponseDataset:
        """Create from qr pairs."""
        # define ids as simple integers
        queries = {str(idx): query for idx, (query, _) in enumerate(qr_pairs)}
        responses = {str(idx): response for idx, (_, response) in enumerate(qr_pairs)}
        return cls(queries=queries, responses=responses)

    @property
    def qr_pairs(self) -> List[Tuple[str, str]]:
        """Get pairs."""
        # if query_id not in response, throw error
        for query_id in self.queries:
            if query_id not in self.responses:
                raise ValueError(f"Query id {query_id} not in responses")

        return [
            (self.queries[query_id], self.responses[query_id])
            for query_id in self.queries
        ]

    @property
    def questions(self) -> List[str]:
        """Get questions."""
        return list(self.queries.values())

    def save_json(self, path: str) -> None:
        """Save json."""
        with open(path, "w") as f:
            json.dump(self.dict(), f, indent=4)

    @classmethod
    def from_json(cls, path: str) -> QueryResponseDataset:
        """Load json."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
