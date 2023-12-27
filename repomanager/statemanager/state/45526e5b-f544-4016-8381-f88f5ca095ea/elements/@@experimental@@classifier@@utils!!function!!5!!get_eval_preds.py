def get_eval_preds(
    train_prompt: BasePromptTemplate, train_str: str, eval_df: pd.DataFrame, n: int = 20
) -> List:
    """Get eval preds."""
    llm = OpenAI()
    eval_preds = []
    for i in range(n):
        eval_str = get_sorted_dict_str(eval_df.iloc[i].to_dict())
        response = llm.predict(train_prompt, train_str=train_str, eval_str=eval_str)
        pred = extract_float_given_response(response)
        print(f"Getting preds: {i}/{n}: {pred}")
        if pred is None:
            # something went wrong, impute a 0.5
            eval_preds.append(0.5)
        else:
            eval_preds.append(pred)
    return eval_preds
