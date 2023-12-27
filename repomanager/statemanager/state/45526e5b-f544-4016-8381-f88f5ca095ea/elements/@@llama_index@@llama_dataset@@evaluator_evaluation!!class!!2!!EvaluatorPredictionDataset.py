class EvaluatorPredictionDataset(BaseLlamaPredictionDataset):
    """Evaluation Prediction Dataset Class."""

    _prediction_type = EvaluatorExamplePrediction

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data = {}
        if self.predictions:
            data = {
                "feedback": [t.feedback for t in self.predictions],
                "score": [t.score for t in self.predictions],
            }

        return PandasDataFrame(data)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "EvaluatorPredictionDataset"
