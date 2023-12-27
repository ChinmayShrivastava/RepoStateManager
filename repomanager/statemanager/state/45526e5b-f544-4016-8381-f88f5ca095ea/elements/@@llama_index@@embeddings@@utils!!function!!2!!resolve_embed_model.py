def resolve_embed_model(embed_model: Optional[EmbedType] = None) -> BaseEmbedding:
    """Resolve embed model."""
    try:
        from llama_index.bridge.langchain import Embeddings as LCEmbeddings
    except ImportError:
        LCEmbeddings = None  # type: ignore

    if embed_model == "default":
        try:
            embed_model = OpenAIEmbedding()
            validate_openai_api_key(embed_model.api_key)
        except ValueError as e:
            raise ValueError(
                "\n******\n"
                "Could not load OpenAI embedding model. "
                "If you intended to use OpenAI, please check your OPENAI_API_KEY.\n"
                "Original error:\n"
                f"{e!s}"
                "\nConsider using embed_model='local'.\n"
                "Visit our documentation for more embedding options: "
                "https://docs.llamaindex.ai/en/stable/module_guides/models/"
                "embeddings.html#modules"
                "\n******"
            )

    # for image embeddings
    if embed_model == "clip":
        embed_model = ClipEmbedding()

    if isinstance(embed_model, str):
        splits = embed_model.split(":", 1)
        is_local = splits[0]
        model_name = splits[1] if len(splits) > 1 else None
        if is_local != "local":
            raise ValueError(
                "embed_model must start with str 'local' or of type BaseEmbedding"
            )

        cache_folder = os.path.join(get_cache_dir(), "models")
        os.makedirs(cache_folder, exist_ok=True)

        if model_name in INSTRUCTOR_MODELS:
            embed_model = InstructorEmbedding(
                model_name=model_name, cache_folder=cache_folder
            )
        else:
            embed_model = HuggingFaceEmbedding(
                model_name=model_name, cache_folder=cache_folder
            )

    if LCEmbeddings is not None and isinstance(embed_model, LCEmbeddings):
        embed_model = LangchainEmbedding(embed_model)

    if embed_model is None:
        print("Embeddings have been explicitly disabled. Using MockEmbedding.")
        embed_model = MockEmbedding(embed_dim=1)

    return embed_model
