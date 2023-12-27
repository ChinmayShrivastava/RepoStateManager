class BaseRetrievalEvaluator(BaseModel):
    """Base Retrieval Evaluator class."""

    metrics: List[BaseRetrievalMetric] = Field(
        ..., description="List of metrics to evaluate"
    )

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_metric_names(
        cls, metric_names: List[str], **kwargs: Any
    ) -> "BaseRetrievalEvaluator":
        """Create evaluator from metric names.

        Args:
            metric_names (List[str]): List of metric names
            **kwargs: Additional arguments for the evaluator

        """
        metric_types = resolve_metrics(metric_names)
        return cls(metrics=[metric() for metric in metric_types], **kwargs)

    @abstractmethod
    async def _aget_retrieved_ids_and_texts(
        self, query: str, mode: RetrievalEvalMode = RetrievalEvalMode.TEXT
    ) -> Tuple[List[str], List[str]]:
        """Get retrieved ids and texts."""
        raise NotImplementedError

    def evaluate(
        self,
        query: str,
        expected_ids: List[str],
        expected_texts: Optional[List[str]] = None,
        mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
        **kwargs: Any,
    ) -> RetrievalEvalResult:
        """Run evaluation results with query string and expected ids.

        Args:
            query (str): Query string
            expected_ids (List[str]): Expected ids

        Returns:
            RetrievalEvalResult: Evaluation result

        """
        return asyncio.run(
            self.aevaluate(
                query=query,
                expected_ids=expected_ids,
                expected_texts=expected_texts,
                mode=mode,
                **kwargs,
            )
        )

    # @abstractmethod
    async def aevaluate(
        self,
        query: str,
        expected_ids: List[str],
        expected_texts: Optional[List[str]] = None,
        mode: RetrievalEvalMode = RetrievalEvalMode.TEXT,
        **kwargs: Any,
    ) -> RetrievalEvalResult:
        """Run evaluation with query string, retrieved contexts,
        and generated response string.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        retrieved_ids, retrieved_texts = await self._aget_retrieved_ids_and_texts(
            query, mode
        )
        metric_dict = {}
        for metric in self.metrics:
            eval_result = metric.compute(
                query, expected_ids, retrieved_ids, expected_texts, retrieved_texts
            )
            metric_dict[metric.metric_name] = eval_result

        return RetrievalEvalResult(
            query=query,
            expected_ids=expected_ids,
            expected_texts=expected_texts,
            retrieved_ids=retrieved_ids,
            retrieved_texts=retrieved_texts,
            mode=mode,
            metric_dict=metric_dict,
        )

    async def aevaluate_dataset(
        self,
        dataset: EmbeddingQAFinetuneDataset,
        workers: int = 2,
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[RetrievalEvalResult]:
        """Run evaluation with dataset."""
        semaphore = asyncio.Semaphore(workers)

        async def eval_worker(
            query: str, expected_ids: List[str], mode: RetrievalEvalMode
        ) -> RetrievalEvalResult:
            async with semaphore:
                return await self.aevaluate(query, expected_ids=expected_ids, mode=mode)

        response_jobs = []
        mode = RetrievalEvalMode.from_str(dataset.mode)
        for query_id, query in dataset.queries.items():
            expected_ids = dataset.relevant_docs[query_id]
            response_jobs.append(eval_worker(query, expected_ids, mode))
        if show_progress:
            from tqdm.asyncio import tqdm_asyncio

            eval_results = await tqdm_asyncio.gather(*response_jobs)
        else:
            eval_results = await asyncio.gather(*response_jobs)

        return eval_results