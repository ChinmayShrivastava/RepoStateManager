class HotpotQAEvaluator:
    """
    Refer to https://hotpotqa.github.io/ for more details on the dataset.
    """

    def _download_datasets(self) -> Dict[str, str]:
        cache_dir = get_cache_dir()

        dataset_paths = {}
        dataset = "hotpot_dev_distractor"
        dataset_full_path = os.path.join(cache_dir, "datasets", "HotpotQA")
        if not os.path.exists(dataset_full_path):
            url = DEV_DISTRACTOR_URL
            try:
                os.makedirs(dataset_full_path, exist_ok=True)
                save_file = open(
                    os.path.join(dataset_full_path, "dev_distractor.json"), "wb"
                )
                response = requests.get(url, stream=True)

                # Define the size of each chunk
                chunk_size = 1024

                # Loop over the chunks and parse the JSON data
                for chunk in tqdm.tqdm(response.iter_content(chunk_size=chunk_size)):
                    if chunk:
                        save_file.write(chunk)
            except Exception as e:
                if os.path.exists(dataset_full_path):
                    print(
                        "Dataset:", dataset, "not found at:", url, "Removing cached dir"
                    )
                    rmtree(dataset_full_path)
                raise ValueError(f"could not download {dataset} dataset") from e
        dataset_paths[dataset] = os.path.join(dataset_full_path, "dev_distractor.json")
        print("Dataset:", dataset, "downloaded at:", dataset_full_path)
        return dataset_paths

    def run(
        self,
        query_engine: BaseQueryEngine,
        queries: int = 10,
        queries_fraction: Optional[float] = None,
        show_result: bool = False,
    ) -> None:
        dataset_paths = self._download_datasets()
        dataset = "hotpot_dev_distractor"
        dataset_path = dataset_paths[dataset]
        print("Evaluating on dataset:", dataset)
        print("-------------------------------------")

        f = open(dataset_path)
        query_objects = json.loads(f.read())
        if queries_fraction:
            queries_to_load = int(len(query_objects) * queries_fraction)
        else:
            queries_to_load = queries
            queries_fraction = round(queries / len(query_objects), 5)

        print(
            f"Loading {queries_to_load} queries out of \
{len(query_objects)} (fraction: {queries_fraction})"
        )
        query_objects = query_objects[:queries_to_load]

        assert isinstance(
            query_engine, RetrieverQueryEngine
        ), "query_engine must be a RetrieverQueryEngine for this evaluation"
        retriever = HotpotQARetriever(query_objects)
        # Mock the query engine with a retriever
        query_engine = query_engine.with_retriever(retriever=retriever)

        scores = {"exact_match": 0.0, "f1": 0.0}

        for query in query_objects:
            query_bundle = QueryBundle(
                query_str=query["question"]
                + " Give a short factoid answer (as few words as possible).",
                custom_embedding_strs=[query["question"]],
            )
            response = query_engine.query(query_bundle)
            em = int(
                exact_match_score(
                    prediction=str(response), ground_truth=query["answer"]
                )
            )
            f1, _, _ = f1_score(prediction=str(response), ground_truth=query["answer"])
            scores["exact_match"] += em
            scores["f1"] += f1
            if show_result:
                print("Question: ", query["question"])
                print("Response:", response)
                print("Correct answer: ", query["answer"])
                print("EM:", em, "F1:", f1)
                print("-------------------------------------")

        for score in scores:
            scores[score] /= len(query_objects)

        print("Scores: ", scores)
