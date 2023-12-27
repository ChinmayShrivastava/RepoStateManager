class HybridFusionCallable(Protocol):
    """Hybrid fusion callable protocol."""

    def __call__(
        self,
        dense_result: VectorStoreQueryResult,
        sparse_result: VectorStoreQueryResult,
        **kwargs: Any,
    ) -> VectorStoreQueryResult:
        """Hybrid fusion callable."""
        ...
