class ParamTuner(BaseParamTuner):
    """Parameter tuner.

    Args:
        param_dict(Dict): A dictionary of parameters to iterate over.
            Example param_dict:
            {
                "num_epochs": [10, 20],
                "batch_size": [8, 16, 32],
            }
        fixed_param_dict(Dict): A dictionary of fixed parameters passed to each job.

    """

    param_fn: Callable[[Dict[str, Any]], RunResult] = Field(
        ..., description="Function to run with parameters."
    )

    def tune(self) -> TunedResult:
        """Run tuning."""
        # each key in param_dict is a parameter to tune, each val
        # is a list of values to try
        # generate combinations of parameters from the param_dict
        param_combinations = generate_param_combinations(self.param_dict)

        # for each combination, run the job with the arguments
        # in args_dict

        combos_with_progress = enumerate(
            get_tqdm_iterable(
                param_combinations, self.show_progress, "Param combinations."
            )
        )

        all_run_results = []
        for idx, param_combination in combos_with_progress:
            full_param_dict = {
                **self.fixed_param_dict,
                **param_combination,
            }
            run_result = self.param_fn(full_param_dict)

            all_run_results.append(run_result)

        # sort the results by score
        sorted_run_results = sorted(
            all_run_results, key=lambda x: x.score, reverse=True
        )

        return TunedResult(run_results=sorted_run_results, best_idx=0)
