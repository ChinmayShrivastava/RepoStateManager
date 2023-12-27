class LabelledRagDataset(BaseLlamaDataset[BaseQueryEngine]):
    """RagDataset class."""

    _example_type = LabelledRagDataExample

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data = {
            "query": [t.query for t in self.examples],
            "reference_contexts": [t.reference_contexts for t in self.examples],
            "reference_answer": [t.reference_answer for t in self.examples],
            "reference_answer_by": [str(t.reference_answer_by) for t in self.examples],
            "query_by": [str(t.query_by) for t in self.examples],
        }

        return PandasDataFrame(data)

    async def _apredict_example(
        self,
        predictor: BaseQueryEngine,
        example: LabelledRagDataExample,
        sleep_time_in_seconds: int,
    ) -> RagExamplePrediction:
        """Async predict RAG example with a query engine."""
        await asyncio.sleep(sleep_time_in_seconds)
        response = await predictor.aquery(example.query)
        return RagExamplePrediction(
            response=str(response), contexts=[s.text for s in response.source_nodes]
        )

    def _predict_example(
        self,
        predictor: BaseQueryEngine,
        example: LabelledRagDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> RagExamplePrediction:
        """Predict RAG example with a query engine."""
        time.sleep(sleep_time_in_seconds)
        response = predictor.query(example.query)
        return RagExamplePrediction(
            response=str(response), contexts=[s.text for s in response.source_nodes]
        )

    def _construct_prediction_dataset(
        self, predictions: List[RagExamplePrediction]
    ) -> RagPredictionDataset:
        """Construct prediction dataset."""
        return RagPredictionDataset(predictions=predictions)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "LabelledRagDataset"
