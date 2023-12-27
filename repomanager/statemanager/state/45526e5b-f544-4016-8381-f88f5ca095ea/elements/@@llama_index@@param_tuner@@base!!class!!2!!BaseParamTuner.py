class BaseParamTuner(BaseModel):
    """Base param tuner."""

    param_dict: Dict[str, Any] = Field(
        ..., description="A dictionary of parameters to iterate over."
    )
    fixed_param_dict: Dict[str, Any] = Field(
        default_factory=dict,
        description="A dictionary of fixed parameters passed to each job.",
    )
    show_progress: bool = False

    @abstractmethod
    def tune(self) -> TunedResult:
        """Tune parameters."""

    async def atune(self) -> TunedResult:
        """Async Tune parameters.

        Override if you implement a native async method.

        """
        return self.tune()
