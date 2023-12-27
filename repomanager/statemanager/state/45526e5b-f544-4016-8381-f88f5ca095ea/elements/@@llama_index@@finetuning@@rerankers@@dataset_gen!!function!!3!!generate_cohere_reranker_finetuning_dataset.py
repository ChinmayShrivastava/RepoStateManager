def generate_cohere_reranker_finetuning_dataset(
    query_context_pairs: EmbeddingQAFinetuneDataset,
    num_negatives: int = 0,
    top_k_dissimilar: int = 100,
    hard_negatives_gen_method: str = "random",
    finetune_dataset_file_name: str = "train.jsonl",
    embed_model: Optional[Any] = None,
) -> Any:
    queries, relevant_contexts = get_query_context_lists(query_context_pairs)

    if num_negatives:
        hard_negatives = generate_hard_negatives(
            queries,
            relevant_contexts,
            embed_model,
            num_negatives,
            hard_negatives_gen_method,
        )
    else:
        hard_negatives = [[] for _ in queries]
    # Open the file in write mode
    with open(finetune_dataset_file_name, "w") as outfile:
        # Iterate over the lists simultaneously using zip
        for query, context, hard_negative in zip(
            queries, relevant_contexts, hard_negatives
        ):
            # Instantiate a CohereRerankerFinetuneDataset object for the current entry
            entry = CohereRerankerFinetuneDataset(
                query=query, relevant_passages=[context], hard_negatives=hard_negative
            )
            # Write the JSONL string to the file
            outfile.write(entry.to_jsonl())
