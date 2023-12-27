def generate_sql(llama_indexes: dict, examples: list, output_file: str) -> None:
    """Generate SQL queries for the given examples and write them to the output file."""
    with open(output_file, "w") as f:
        for example in tqdm(examples, desc=f"Generating {output_file}"):
            db_name = example["db_id"]
            nl_query_text = example["question"]
            try:
                sql_query = _generate_sql(llama_indexes[db_name], nl_query_text)
            except Exception as e:
                print(
                    f"Failed to generate SQL query for question: "
                    f"{example['question']} on database: {example['db_id']}."
                )
                print(e)
                sql_query = "ERROR"
            f.write(sql_query + "\n")
