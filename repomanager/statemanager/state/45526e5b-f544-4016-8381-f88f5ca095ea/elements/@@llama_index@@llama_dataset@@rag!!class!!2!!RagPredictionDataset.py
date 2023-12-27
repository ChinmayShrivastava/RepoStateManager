class RagPredictionDataset(BaseLlamaPredictionDataset):
    """RagDataset class."""

    _prediction_type = RagExamplePrediction

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data = {}
        if self.predictions:
            data = {
                "response": [t.response for t in self.predictions],
                "contexts": [t.contexts for t in self.predictions],
            }

        return PandasDataFrame(data)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "RagPredictionDataset"
