def generate_ce_fine_tuning_dataset(
    documents: List[Document],
    questions_list: List[str],
    max_chunk_length: int = 1000,
    llm: Optional[LLM] = None,
    qa_doc_relevance_prompt: str = DEFAULT_QUERY_DOC_RELEVANCE_PROMPT,
    top_k: int = 8,
) -> List[CrossEncoderFinetuningDatasetSample]:
    ce_dataset_list = []

    node_parser = TokenTextSplitter(
        separator=" ",
        chunk_size=max_chunk_length,
        chunk_overlap=0,
        backup_separators=["\n"],
        tokenizer=get_tokenizer(),
    )

    # Use logit bias in case of OpenAI for the tokens for Yes and No
    # to decrease the likelihood of any other tokens occurring
    llm = llm or OpenAI(
        model="gpt-3.5-turbo-16k", temperature=0.1, logit_bias={9642: 1, 2822: 1}
    )

    nodes = node_parser.get_nodes_from_documents(documents, show_progress=False)

    index = VectorStoreIndex(nodes)
    retriever = index.as_retriever(similarity_top_k=top_k)

    for question in tqdm(questions_list):
        if question != "":
            retrieved_nodes = retriever.retrieve(question)
            for node in retrieved_nodes:
                node_content = node.get_text()
                msg_prompt = qa_doc_relevance_prompt.format(
                    query=question, document=node_content
                )
                response = llm.complete(msg_prompt)
                result = response.text.strip().lower()

                if result == "yes":
                    question_row = CrossEncoderFinetuningDatasetSample(
                        query=question, context=node_content, score=1
                    )
                    ce_dataset_list.append(question_row)
                elif result == "no":
                    question_row = CrossEncoderFinetuningDatasetSample(
                        query=question, context=node_content, score=0
                    )
                    ce_dataset_list.append(question_row)
                else:
                    pass

    return ce_dataset_list
