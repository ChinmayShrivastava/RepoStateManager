class TunedResult(BaseModel):
    run_results: List[RunResult]
    best_idx: int

    @property
    def best_run_result(self) -> RunResult:
        """Get best run result."""
        return self.run_results[self.best_idx]
