def bench_simple_vector_store(
    embed_models: List[Callable[[int], Tuple[BaseEmbedding, str, int]]],
    num_strings: List[int] = [100],
    string_lengths: List[int] = [64, 256],
    embed_batch_sizes: List[int] = [1, DEFAULT_EMBED_BATCH_SIZE],
    torch_num_threads: Optional[int] = None,
) -> None:
    """Benchmark embeddings."""
    print("Benchmarking Embeddings\n---------------------------")

    results = []

    if torch_num_threads is not None:
        import torch

        torch.set_num_threads(torch_num_threads)

    max_num_strings = max(num_strings)
    for string_length in string_lengths:
        generated_strings = generate_strings(
            num_strings=max_num_strings, string_length=string_length
        )

        for string_count in num_strings:
            strings = generated_strings[:string_count]

            for batch_size in embed_batch_sizes:
                models = []
                for create_model in embed_models:
                    models.append(create_model(batch_size=batch_size))  # type: ignore

                for model in models:
                    time1 = time.time()
                    _ = model[0].get_text_embedding_batch(strings, show_progress=True)

                    time2 = time.time()
                    print(
                        f"Embedding with model {model[1]} with "
                        f"batch size {batch_size} and max_seq_length {model[2]} for "
                        f"{string_count} strings of length {string_length} took "
                        f"{time2 - time1} seconds."
                    )
                    results.append((model[1], batch_size, string_length, time2 - time1))
                # TODO: async version

    # print final results
    print("\n\nFinal Results\n---------------------------")
    results_df = pd.DataFrame(
        results, columns=["model", "batch_size", "string_length", "time"]
    )
    print(results_df)
