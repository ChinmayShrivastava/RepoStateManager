class RayTuneParamTuner(BaseParamTuner):
    """Parameter tuner powered by Ray Tune.

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

    run_config_dict: Optional[dict] = Field(
        default=None, description="Run config dict for Ray Tune."
    )

    def tune(self) -> TunedResult:
        """Run tuning."""
        from ray import tune
        from ray.train import RunConfig

        # convert every array in param_dict to a tune.grid_search
        ray_param_dict = {}
        for param_name, param_vals in self.param_dict.items():
            ray_param_dict[param_name] = tune.grid_search(param_vals)

        def param_fn_wrapper(
            ray_param_dict: Dict, fixed_param_dict: Optional[Dict] = None
        ) -> Dict:
            # need a wrapper to pass in parameters to tune + fixed params
            fixed_param_dict = fixed_param_dict or {}
            full_param_dict = {
                **fixed_param_dict,
                **ray_param_dict,
            }
            tuned_result = self.param_fn(full_param_dict)
            # need to convert RunResult to dict to obey
            # Ray Tune's API
            return tuned_result.dict()

        run_config = RunConfig(**self.run_config_dict) if self.run_config_dict else None

        tuner = tune.Tuner(
            tune.with_parameters(
                param_fn_wrapper, fixed_param_dict=self.fixed_param_dict
            ),
            param_space=ray_param_dict,
            run_config=run_config,
        )

        results = tuner.fit()
        all_run_results = []
        for idx in range(len(results)):
            result = results[idx]
            # convert dict back to RunResult (reconstruct it with metadata)
            # get the keys in RunResult, assign corresponding values in
            # result.metrics to those keys
            run_result = RunResult.parse_obj(result.metrics)
            # add some more metadata to run_result (e.g. timestamp)
            run_result.metadata["timestamp"] = (
                result.metrics["timestamp"] if result.metrics else None
            )

            all_run_results.append(run_result)

        # sort the results by score
        sorted_run_results = sorted(
            all_run_results, key=lambda x: x.score, reverse=True
        )

        return TunedResult(run_results=sorted_run_results, best_idx=0)
