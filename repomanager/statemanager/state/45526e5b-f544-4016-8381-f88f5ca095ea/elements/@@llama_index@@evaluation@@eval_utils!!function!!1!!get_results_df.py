def get_results_df(
    eval_results_list: List[EvaluationResult], names: List[str], metric_keys: List[str]
) -> pd.DataFrame:
    """Get results df.

    Args:
        eval_results_list (List[EvaluationResult]):
            List of evaluation results.
        names (List[str]):
            Names of the evaluation results.
        metric_keys (List[str]):
            List of metric keys to get.

    """
    metric_dict = defaultdict(list)
    metric_dict["names"] = names
    for metric_key in metric_keys:
        for eval_results in eval_results_list:
            mean_score = np.array([r.score for r in eval_results[metric_key]]).mean()
            metric_dict[metric_key].append(mean_score)
    return pd.DataFrame(metric_dict)
