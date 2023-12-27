def get_query_context_lists(
    query_context_pairs: EmbeddingQAFinetuneDataset,
) -> Tuple[List[str], List[str]]:
    queries = []
    relevant_contexts = []

    # 'query_context_pairs' is an object with 'queries', 'corpus', and 'relevant_docs' attributes
    for query_id, query in query_context_pairs.queries.items():
        # Get the first relevant document ID for the current query
        relevant_doc_id = query_context_pairs.relevant_docs[query_id][0]
        # Get the relevant context using the relevant document ID
        relevant_context = query_context_pairs.corpus[relevant_doc_id]
        # Append the query and the relevant context to their respective lists
        queries.append(query)
        relevant_contexts.append(relevant_context)

    return queries, relevant_contexts
