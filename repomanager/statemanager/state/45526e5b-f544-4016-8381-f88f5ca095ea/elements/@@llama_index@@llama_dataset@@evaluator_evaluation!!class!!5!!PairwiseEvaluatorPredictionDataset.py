class PairwiseEvaluatorPredictionDataset(BaseLlamaPredictionDataset):
    """Pairwise evaluation predictions dataset class."""

    _prediction_type = PairwiseEvaluatorExamplePrediction

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data = {}
        if self.predictions:
            data = {
                "feedback": [t.feedback for t in self.predictions],
                "score": [t.score for t in self.predictions],
                "ordering": [t.evaluation_source.value for t in self.predictions],
            }

        return PandasDataFrame(data)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "PairwiseEvaluatorPredictionDataset"
