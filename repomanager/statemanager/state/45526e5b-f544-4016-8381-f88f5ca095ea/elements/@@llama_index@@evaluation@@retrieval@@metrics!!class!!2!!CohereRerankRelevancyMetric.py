class CohereRerankRelevancyMetric(BaseRetrievalMetric):
    """Cohere rerank relevancy metric."""

    model: str = Field(description="Cohere model name.")
    metric_name: str = "cohere_rerank_relevancy"

    _client: Any = PrivateAttr()

    def __init__(
        self,
        model: str = "rerank-english-v2.0",
        api_key: Optional[str] = None,
    ):
        try:
            api_key = api_key or os.environ["COHERE_API_KEY"]
        except IndexError:
            raise ValueError(
                "Must pass in cohere api key or "
                "specify via COHERE_API_KEY environment variable "
            )
        try:
            from cohere import Client
        except ImportError:
            raise ImportError(
                "Cannot import cohere package, please `pip install cohere`."
            )

        self._client = Client(api_key=api_key)
        super().__init__(model=model)

    def _get_agg_func(self, agg: Literal["max", "median", "mean"]) -> Callable:
        """Get agg func."""
        return _AGG_FUNC[agg]

    def compute(
        self,
        query: Optional[str] = None,
        expected_ids: Optional[List[str]] = None,
        retrieved_ids: Optional[List[str]] = None,
        expected_texts: Optional[List[str]] = None,
        retrieved_texts: Optional[List[str]] = None,
        agg: Literal["max", "median", "mean"] = "max",
        **kwargs: Any,
    ) -> RetrievalMetricResult:
        """Compute metric."""
        del expected_texts  # unused

        if retrieved_texts is None:
            raise ValueError("Retrieved texts must be provided")

        results = self._client.rerank(
            model=self.model,
            top_n=len(
                retrieved_texts
            ),  # i.e. get a rank score for each retrieved chunk
            query=query,
            documents=retrieved_texts,
        )
        relevance_scores = [r.relevance_score for r in results]
        agg_func = self._get_agg_func(agg)

        return RetrievalMetricResult(
            score=agg_func(relevance_scores), metadata={"agg": agg}
        )
