def _get_answers(
    llm: OpenAI,
    indexes: Dict[str, SQLStructStoreIndex],
    db_names: List[str],
    sql_queries: List[str],
    examples: List[dict],
    output_filename: str,
    use_cache: bool,
) -> List[dict]:
    if use_cache and os.path.exists(output_filename):
        with open(output_filename) as f:
            return json.load(f)

    results = []
    for db_name, sql_query, example in tqdm(
        list(zip(db_names, sql_queries, examples)),
        desc=f"Getting NL Answers to: {output_filename}",
    ):
        assert example["db_id"] == db_name
        question = example["question"]
        result = {
            "question": question,
            "sql_query": sql_query,
            "sql_result": None,
            "answer": None,
        }
        results.append(result)
        if sql_query.strip() == "ERROR":
            result["sql_result"] = "ERROR"
            result["answer"] = "ERROR"
        try:
            query_engine = indexes[db_name].as_query_engine(query_mode=SQLQueryMode.SQL)
            resp = query_engine.query(sql_query)
            assert isinstance(resp, Response)
            result["sql_result"] = resp.response
            if resp.response is None:
                result["answer"] = ""
            result["answer"] = _answer(llm, question, sql_query, resp.response)
        except Exception as e:
            print(f"Error encountered when answering question ({question}): {e}")
    with open(output_filename, "w") as f:
        json.dump(results, f, indent=2)
    return results
