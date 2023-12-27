class BaseLlamaPredictionDataset(BaseModel):
    _prediction_type: Type[BaseLlamaExamplePrediction] = BaseLlamaExamplePrediction  # type: ignore[misc]
    predictions: List[BaseLlamaExamplePrediction] = Field(
        default=list, description="Predictions on train_examples."
    )

    def __getitem__(self, val: Union[slice, int]) -> List[BaseLlamaExamplePrediction]:
        """Enable slicing and indexing.

        Returns the desired slice on `predictions`.
        """
        return self.predictions[val]

    @abstractmethod
    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""

    def save_json(self, path: str) -> None:
        """Save json."""
        with open(path, "w") as f:
            predictions = None
            if self.predictions:
                predictions = [
                    self._prediction_type.dict(el) for el in self.predictions
                ]
            data = {
                "predictions": predictions,
            }

            json.dump(data, f, indent=4)

    @classmethod
    def from_json(cls, path: str) -> "BaseLlamaPredictionDataset":
        """Load json."""
        with open(path) as f:
            data = json.load(f)

        predictions = [cls._prediction_type.parse_obj(el) for el in data["predictions"]]

        return cls(
            predictions=predictions,
        )

    @property
    @abstractmethod
    def class_name(self) -> str:
        """Class name."""
        return "BaseLlamaPredictionDataset"
