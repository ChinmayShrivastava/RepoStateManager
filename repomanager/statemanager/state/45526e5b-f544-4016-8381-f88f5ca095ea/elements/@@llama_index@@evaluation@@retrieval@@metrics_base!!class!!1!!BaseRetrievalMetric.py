class BaseRetrievalMetric(BaseModel, ABC):
    """Base class for retrieval metrics."""

    metric_name: str

    @abstractmethod
    def compute(
        self,
        query: Optional[str] = None,
        expected_ids: Optional[List[str]] = None,
        retrieved_ids: Optional[List[str]] = None,
        expected_texts: Optional[List[str]] = None,
        retrieved_texts: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> RetrievalMetricResult:
        """Compute metric.

        Args:
            query (Optional[str]): Query string
            expected_ids (Optional[List[str]]): Expected ids
            retrieved_ids (Optional[List[str]]): Retrieved ids
            **kwargs: Additional keyword arguments

        """

    class Config:
        arbitrary_types_allowed = True
