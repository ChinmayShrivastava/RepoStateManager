class AsyncParamTuner(BaseParamTuner):
    """Async Parameter tuner.

    Args:
        param_dict(Dict): A dictionary of parameters to iterate over.
            Example param_dict:
            {
                "num_epochs": [10, 20],
                "batch_size": [8, 16, 32],
            }
        fixed_param_dict(Dict): A dictionary of fixed parameters passed to each job.
        aparam_fn (Callable): An async function to run with parameters.
        num_workers (int): Number of workers to use.

    """

    aparam_fn: Callable[[Dict[str, Any]], Awaitable[RunResult]] = Field(
        ..., description="Async function to run with parameters."
    )
    num_workers: int = Field(2, description="Number of workers to use.")

    _semaphore: asyncio.Semaphore = PrivateAttr()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._semaphore = asyncio.Semaphore(self.num_workers)

    async def atune(self) -> TunedResult:
        """Run tuning."""
        # each key in param_dict is a parameter to tune, each val
        # is a list of values to try
        # generate combinations of parameters from the param_dict
        param_combinations = generate_param_combinations(self.param_dict)

        # for each combination, run the job with the arguments
        # in args_dict

        async def aparam_fn_worker(
            semaphore: asyncio.Semaphore,
            full_param_dict: Dict[str, Any],
        ) -> RunResult:
            """Async param fn worker."""
            async with semaphore:
                return await self.aparam_fn(full_param_dict)

        all_run_results = []
        run_jobs = []
        for param_combination in param_combinations:
            full_param_dict = {
                **self.fixed_param_dict,
                **param_combination,
            }
            run_jobs.append(aparam_fn_worker(self._semaphore, full_param_dict))
            # run_jobs.append(self.aparam_fn(full_param_dict))

        if self.show_progress:
            from tqdm.asyncio import tqdm_asyncio

            all_run_results = await tqdm_asyncio.gather(*run_jobs)
        else:
            all_run_results = await asyncio.gather(*run_jobs)

        # sort the results by score
        sorted_run_results = sorted(
            all_run_results, key=lambda x: x.score, reverse=True
        )

        return TunedResult(run_results=sorted_run_results, best_idx=0)

    def tune(self) -> TunedResult:
        """Run tuning."""
        return asyncio.run(self.atune())
