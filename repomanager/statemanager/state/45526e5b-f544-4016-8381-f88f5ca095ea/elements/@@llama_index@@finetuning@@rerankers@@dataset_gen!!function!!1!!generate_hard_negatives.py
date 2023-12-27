def generate_hard_negatives(
    queries: List[str],
    relevant_contexts: List[str],
    embed_model: Optional[Any],
    num_negatives: int = 5,
    method: str = "random",
) -> Any:
    hard_negatives = []

    if method == "cosine_similarity":
        query_embeddings = [
            generate_embeddings(embed_model, query) for query in queries
        ]
        relevant_contexts_embeddings = [
            generate_embeddings(embed_model, context) for context in relevant_contexts
        ]

    for query_index, _ in enumerate(queries):
        if method == "random":
            # Exclude the correct context
            potential_negatives = (
                relevant_contexts[:query_index] + relevant_contexts[query_index + 1 :]
            )
            # Randomly select hard negatives
            hard_negatives.append(
                random.sample(
                    potential_negatives, min(num_negatives, len(potential_negatives))
                )
            )

        elif method == "cosine_similarity":
            query_embedding = query_embeddings[query_index]
            # Use get_top_k_embeddings to select num_negatives closest but not correct contexts
            _, relevant_contexts_indices = get_top_k_embeddings(
                query_embedding,
                relevant_contexts_embeddings,
            )

            # Filter out the correct context to only include hard negatives
            hard_negative_indices = [
                idx for idx in relevant_contexts_indices if idx != query_index
            ][:num_negatives]

            # Map indices to actual contexts to get the hard negatives
            hard_negatives_for_query = [
                relevant_contexts[idx] for idx in hard_negative_indices
            ]

            hard_negatives.append(hard_negatives_for_query)
    return hard_negatives
