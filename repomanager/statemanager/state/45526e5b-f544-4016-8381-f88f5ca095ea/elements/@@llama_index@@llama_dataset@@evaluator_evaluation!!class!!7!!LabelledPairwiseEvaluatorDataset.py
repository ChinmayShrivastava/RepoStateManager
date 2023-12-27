class LabelledPairwiseEvaluatorDataset(BaseLlamaDataset[BaseEvaluator]):
    """Labelled pairwise evaluation dataset. For evaluating the evaluator in
    performing pairwise evaluations.

    Args:
        BaseLlamaDataset (_type_): _description_
    """

    _example_type = LabelledPairwiseEvaluatorDataExample

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data = {
            "query": [t.query for t in self.examples],
            "answer": [t.answer for t in self.examples],
            "second_answer": [t.second_answer for t in self.examples],
            "contexts": [t.contexts for t in self.examples],
            "ground_truth_answer": [t.ground_truth_answer for t in self.examples],
            "query_by": [str(t.query_by) for t in self.examples],
            "answer_by": [str(t.answer_by) for t in self.examples],
            "second_answer_by": [str(t.second_answer_by) for t in self.examples],
            "ground_truth_answer_by": [
                str(t.ground_truth_answer_by) for t in self.examples
            ],
            "reference_feedback": [t.reference_feedback for t in self.examples],
            "reference_score": [t.reference_score for t in self.examples],
            "reference_evaluation_by": [
                t.reference_evaluation_by for t in self.examples
            ],
        }

        return PandasDataFrame(data)

    async def _apredict_example(
        self,
        predictor: BaseEvaluator,
        example: LabelledPairwiseEvaluatorDataExample,
        sleep_time_in_seconds: int,
    ) -> PairwiseEvaluatorExamplePrediction:
        """Async predict evaluation example with an Evaluator."""
        await asyncio.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = await predictor.aevaluate(
                query=example.query,
                response=example.answer,
                second_response=example.second_answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return PairwiseEvaluatorExamplePrediction(
                feedback=eval_result.feedback,
                score=eval_result.score,
                evaluation_source=eval_result.pairwise_source,
            )
        else:
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def _predict_example(
        self,
        predictor: BaseEvaluator,
        example: LabelledPairwiseEvaluatorDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> PairwiseEvaluatorExamplePrediction:
        """Predict RAG example with a query engine."""
        time.sleep(sleep_time_in_seconds)
        try:
            eval_result: EvaluationResult = predictor.evaluate(
                query=example.query,
                response=example.answer,
                second_response=example.second_answer,
                contexts=example.contexts,
                reference=example.ground_truth_answer,
                sleep_time_in_seconds=sleep_time_in_seconds,
            )
        except Exception as err:
            # TODO: raise warning here as well
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=f"Caught error {err!s}"
            )

        if not eval_result.invalid_result:
            return PairwiseEvaluatorExamplePrediction(
                feedback=eval_result.feedback,
                score=eval_result.score,
                evaluation_source=eval_result.pairwise_source,
            )
        else:
            return PairwiseEvaluatorExamplePrediction(
                invalid_prediction=True, invalid_reason=eval_result.invalid_reason
            )

    def _construct_prediction_dataset(
        self, predictions: List[PairwiseEvaluatorExamplePrediction]
    ) -> PairwiseEvaluatorPredictionDataset:
        """Construct prediction dataset."""
        return PairwiseEvaluatorPredictionDataset(predictions=predictions)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "LabelledPairwiseEvaluatorDataset"
