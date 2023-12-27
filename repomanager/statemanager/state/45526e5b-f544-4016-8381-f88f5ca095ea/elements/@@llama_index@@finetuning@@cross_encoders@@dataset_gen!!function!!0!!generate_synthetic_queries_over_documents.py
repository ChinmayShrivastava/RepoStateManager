def generate_synthetic_queries_over_documents(
    documents: List[Document],
    num_questions_per_chunk: int = 5,
    max_chunk_length: int = 3000,
    qa_topic: str = "everything",
    llm: Optional[LLM] = None,
    qa_generate_system_msg: str = DEFAULT_QUERY_GEN_SYSTEM_PROMPT,
    qa_generate_user_msg: str = DEFAULT_QUERY_GEN_USER_PROMPT,
) -> List[str]:
    questions = []
    node_parser = TokenTextSplitter(
        separator=" ",
        chunk_size=max_chunk_length,
        chunk_overlap=0,
        backup_separators=["\n"],
        tokenizer=get_tokenizer(),
    )

    llm = llm or OpenAI(model="gpt-3.5-turbo-16k", temperature=0.3)
    nodes = node_parser.get_nodes_from_documents(documents, show_progress=False)

    node_dict = {
        node.node_id: node.get_content(metadata_mode=MetadataMode.NONE)
        for node in nodes
    }

    for node_id, text in tqdm(node_dict.items()):
        system_msg = qa_generate_system_msg.format(
            num_questions_per_chunk=num_questions_per_chunk, qa_topic=qa_topic
        )
        user_msg = qa_generate_user_msg.format(
            num_questions_per_chunk=num_questions_per_chunk, context=text
        )
        messages = [
            ChatMessage(role="system", content=system_msg),
            ChatMessage(role="user", content=user_msg),
        ]
        response = llm.chat(messages)
        response_content: str = (
            response.message.content if response.message.content is not None else ""
        )
        response_questions = re.split(";|\n", response_content)
        questions.extend(response_questions)

    return questions
