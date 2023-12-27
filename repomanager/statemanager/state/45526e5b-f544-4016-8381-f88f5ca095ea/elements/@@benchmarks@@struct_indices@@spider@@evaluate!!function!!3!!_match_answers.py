def _match_answers(
    llm: OpenAI,
    gold_results: List[dict],
    pred_results: List[dict],
    examples: List[dict],
    output_filename: str,
) -> float:
    results = []
    for gold, pred, example in tqdm(
        list(zip(gold_results, pred_results, examples)),
        desc=f"Evaluating: {output_filename}",
    ):
        assert gold["question"] == example["question"]
        assert pred["question"] == example["question"]

        # Match execution results.
        if pred["sql_result"] is None or gold["sql_result"] is None:
            exec_match = None
        elif pred["sql_result"] == "ERROR":
            exec_match = False
        else:
            try:
                p_tuples = set(ast.literal_eval(pred["sql_result"]))
                g_tuples = set(ast.literal_eval(gold["sql_result"]))
                exec_match = p_tuples == g_tuples
            except Exception as e:
                print("Error encountered when parsing SQL result: ", e)
                exec_match = None

        # Match NL answers.
        if pred["answer"] is None or gold["answer"] is None:
            answer_match = None
        elif pred["answer"] == "ERROR":
            answer_match = False
        else:
            answer_match = _match(
                llm, example["question"], gold["answer"], pred["answer"]
            )

        results.append(
            {
                "db": example["db_id"],
                "exec_match": exec_match,
                "answer_match": answer_match,
                "gold": gold,
                "pred": pred,
            }
        )
    valid_results = [
        e
        for e in results
        if e["exec_match"] is not None and e["answer_match"] is not None
    ]
    answer_accuracy = sum(
        [e["exec_match"] or e["answer_match"] for e in valid_results]
    ) / float(len(valid_results))
    with open(output_filename, "w") as f:
        json.dump(
            {
                "answer_accuracy": answer_accuracy,
                "total": len(results),
                "valid": len(valid_results),
                "results": results,
            },
            f,
            indent=2,
        )
    return answer_accuracy
