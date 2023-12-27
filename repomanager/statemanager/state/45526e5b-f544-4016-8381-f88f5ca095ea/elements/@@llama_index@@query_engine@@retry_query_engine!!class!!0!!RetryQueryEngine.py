class RetryQueryEngine(BaseQueryEngine):
    """Does retry on query engine if it fails evaluation.

    Args:
        query_engine (BaseQueryEngine): A query engine object
        evaluator (BaseEvaluator): An evaluator object
        max_retries (int): Maximum number of retries
        callback_manager (Optional[CallbackManager]): A callback manager object
    """

    def __init__(
        self,
        query_engine: BaseQueryEngine,
        evaluator: BaseEvaluator,
        max_retries: int = 3,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        self._query_engine = query_engine
        self._evaluator = evaluator
        self.max_retries = max_retries
        super().__init__(callback_manager)

    def _get_prompt_modules(self) -> PromptMixinType:
        """Get prompt sub-modules."""
        return {"query_engine": self._query_engine, "evaluator": self._evaluator}

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Answer a query."""
        response = self._query_engine._query(query_bundle)
        if self.max_retries <= 0:
            return response
        typed_response = (
            response if isinstance(response, Response) else response.get_response()
        )
        query_str = query_bundle.query_str
        eval = self._evaluator.evaluate_response(query_str, typed_response)
        if eval.passing:
            logger.debug("Evaluation returned True.")
            return response
        else:
            logger.debug("Evaluation returned False.")
            new_query_engine = RetryQueryEngine(
                self._query_engine, self._evaluator, self.max_retries - 1
            )
            query_transformer = FeedbackQueryTransformation()
            new_query = query_transformer.run(query_bundle, {"evaluation": eval})
            return new_query_engine.query(new_query)

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        """Not supported."""
        return self._query(query_bundle)
