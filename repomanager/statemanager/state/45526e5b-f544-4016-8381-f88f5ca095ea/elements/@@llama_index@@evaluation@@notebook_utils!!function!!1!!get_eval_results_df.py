def get_eval_results_df(
    names: List[str], results_arr: List[EvaluationResult], metric: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Organizes EvaluationResults into a deep dataframe and computes the mean
    score.

    result:
        result_df: pd.DataFrame representing all the evaluation results
        mean_df: pd.DataFrame of average scores groupby names
    """
    if len(names) != len(results_arr):
        raise ValueError("names and results_arr must have same length.")

    qs = []
    ss = []
    fs = []
    for res in results_arr:
        qs.append(res.query)
        ss.append(res.score)
        fs.append(res.feedback)

    deep_df = pd.DataFrame({"rag": names, "query": qs, "scores": ss, "feedbacks": fs})
    mean_df = pd.DataFrame(deep_df.groupby(["rag"])["scores"].mean()).T
    if metric:
        mean_df.index = [f"mean_{metric}_score"]

    return deep_df, mean_df
