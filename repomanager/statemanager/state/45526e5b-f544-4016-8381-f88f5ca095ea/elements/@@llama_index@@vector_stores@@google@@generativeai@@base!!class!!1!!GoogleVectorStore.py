class GoogleVectorStore(BasePydanticVectorStore):
    """Google GenerativeAI Vector Store.

    Currently, it computes the embedding vectors on the server side.

    Example:
        google_vector_store = GoogleVectorStore.from_corpus(
                corpus_id="my-corpus-id")
        index = VectorStoreIndex.from_vector_store(
                google_vector_store,
                service_context=google_service_context)

    Attributes:
        corpus_id: The corpus ID that this vector store instance will read and
            write to.
    """

    # Semantic Retriever stores the document node's text as string and embeds
    # the vectors on the server automatically.
    stores_text: bool = True
    is_embedding_query: bool = False

    # This is not the Google's corpus name but an ID generated in the LlamaIndex
    # world.
    corpus_id: str = Field(frozen=True)
    """Corpus ID that this instance of the vector store is using."""

    _client: Any = PrivateAttr()

    def __init__(self, *, client: Any, **kwargs: Any):
        """Raw constructor.

        Use the class method `from_corpus` or `create_corpus` instead.

        Args:
            client: The low-level retriever class from google.ai.generativelanguage.
        """
        try:
            import google.ai.generativelanguage as genai
        except ImportError:
            raise ImportError(_import_err_msg)

        super().__init__(**kwargs)

        assert isinstance(client, genai.RetrieverServiceClient)
        self._client = client

    @classmethod
    def from_corpus(cls, *, corpus_id: str) -> "GoogleVectorStore":
        """Create an instance that points to an existing corpus.

        Args:
            corpus_id: ID of an existing corpus on Google's server.

        Returns:
            An instance of the vector store that points to the specified corpus.

        Raises:
            NoSuchCorpusException if no such corpus is found.
        """
        try:
            import llama_index.vector_stores.google.generativeai.genai_extension as genaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.from_corpus(corpus_id={corpus_id})")
        client = genaix.build_semantic_retriever()
        if genaix.get_corpus(corpus_id=corpus_id, client=client) is None:
            raise NoSuchCorpusException(corpus_id=corpus_id)

        return cls(corpus_id=corpus_id, client=client)

    @classmethod
    def create_corpus(
        cls, *, corpus_id: Optional[str] = None, display_name: Optional[str] = None
    ) -> "GoogleVectorStore":
        """Create an instance that points to a newly created corpus.

        Examples:
            store = GoogleVectorStore.create_corpus()
            print(f"Created corpus with ID: {store.corpus_id})

            store = GoogleVectorStore.create_corpus(
                display_name="My first corpus"
            )

            store = GoogleVectorStore.create_corpus(
                corpus_id="my-corpus-1",
                display_name="My first corpus"
            )

        Args:
            corpus_id: ID of the new corpus to be created. If not provided,
                Google server will provide one for you.
            display_name: Title of the corpus. If not provided, Google server
                will provide one for you.

        Returns:
            An instance of the vector store that points to the specified corpus.

        Raises:
            An exception if the corpus already exists or the user hits the
            quota limit.
        """
        try:
            import llama_index.vector_stores.google.generativeai.genai_extension as genaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(
            f"\n\nGoogleVectorStore.create_corpus(new_corpus_id={corpus_id}, new_display_name={display_name})"
        )

        client = genaix.build_semantic_retriever()
        new_corpus_id = corpus_id or str(uuid.uuid4())
        new_corpus = genaix.create_corpus(
            corpus_id=new_corpus_id, display_name=display_name, client=client
        )
        name = genaix.EntityName.from_str(new_corpus.name)
        return cls(corpus_id=name.corpus_id, client=client)

    @classmethod
    def class_name(cls) -> str:
        return "GoogleVectorStore"

    @property
    def client(self) -> Any:
        return self._client

    def add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        """Add nodes with embedding to vector store.

        If a node has a source node, the source node's ID will be used to create
        a document. Otherwise, a default document for that corpus will be used
        to house the node.

        Furthermore, if the source node has a metadata field "file_name", it
        will be used as the title of the document. If the source node has no
        such field, Google server will assign a title to the document.

        Example:
            store = GoogleVectorStore.from_corpus(corpus_id="123")
            store.add([
                TextNode(
                    text="Hello, my darling",
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id="doc-456",
                            metadata={"file_name": "Title for doc-456"},
                        )
                    },
                ),
                TextNode(
                    text="Goodbye, my baby",
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(
                            node_id="doc-456",
                            metadata={"file_name": "Title for doc-456"},
                        )
                    },
                ),
            ])

        The above code will create one document with ID `doc-456` and title
        `Title for doc-456`. This document will house both nodes.
        """
        try:
            import google.ai.generativelanguage as genai

            import llama_index.vector_stores.google.generativeai.genai_extension as genaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.add(nodes={nodes})")

        client = cast(genai.RetrieverServiceClient, self.client)

        created_node_ids: List[str] = []
        for nodeGroup in _group_nodes_by_source(nodes):
            source = nodeGroup.source_node
            document_id = source.node_id
            document = genaix.get_document(
                corpus_id=self.corpus_id, document_id=document_id, client=client
            )

            if not document:
                genaix.create_document(
                    corpus_id=self.corpus_id,
                    display_name=source.metadata.get("file_name", None),
                    document_id=document_id,
                    metadata=source.metadata,
                    client=client,
                )

            created_chunks = genaix.batch_create_chunk(
                corpus_id=self.corpus_id,
                document_id=document_id,
                texts=[node.get_content() for node in nodeGroup.nodes],
                metadatas=[node.metadata for node in nodeGroup.nodes],
                client=client,
            )
            created_node_ids.extend([chunk.name for chunk in created_chunks])

        return created_node_ids

    def delete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        """Delete nodes by ref_doc_id.

        Both the underlying nodes and the document will be deleted from Google
        server.

        Args:
            ref_doc_id: The document ID to be deleted.
        """
        try:
            import google.ai.generativelanguage as genai

            import llama_index.vector_stores.google.generativeai.genai_extension as genaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.delete(ref_doc_id={ref_doc_id})")

        client = cast(genai.RetrieverServiceClient, self.client)
        genaix.delete_document(
            corpus_id=self.corpus_id, document_id=ref_doc_id, client=client
        )

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        """Query vector store.

        Example:
            store = GoogleVectorStore.from_corpus(corpus_id="123")
            store.query(
                query=VectorStoreQuery(
                    query_str="What is the meaning of life?",
                    # Only nodes with this author.
                    filters=MetadataFilters(
                        filters=[
                            ExactMatchFilter(
                                key="author",
                                value="Arthur Schopenhauer",
                            )
                        ]
                    ),
                    # Only from these docs. If not provided,
                    # the entire corpus is searched.
                    doc_ids=["doc-456"],
                    similarity_top_k=3,
                )
            )

        Args:
            query: See `llama_index.vector_stores.types.VectorStoreQuery`.
        """
        try:
            import google.ai.generativelanguage as genai

            import llama_index.vector_stores.google.generativeai.genai_extension as genaix
        except ImportError:
            raise ImportError(_import_err_msg)

        _logger.debug(f"\n\nGoogleVectorStore.query(query={query})")

        query_str = query.query_str
        if query_str is None:
            raise ValueError("VectorStoreQuery.query_str should not be None.")

        client = cast(genai.RetrieverServiceClient, self.client)

        relevant_chunks: List[genai.RelevantChunk] = []
        if query.doc_ids is None:
            # The chunks from query_corpus should be sorted in reverse order by
            # relevant score.
            relevant_chunks = genaix.query_corpus(
                corpus_id=self.corpus_id,
                query=query_str,
                filter=_convert_filter(query.filters),
                k=query.similarity_top_k,
                client=client,
            )
        else:
            for doc_id in query.doc_ids:
                relevant_chunks.extend(
                    genaix.query_document(
                        corpus_id=self.corpus_id,
                        document_id=doc_id,
                        query=query_str,
                        filter=_convert_filter(query.filters),
                        k=query.similarity_top_k,
                        client=client,
                    )
                )
            # Make sure the chunks are reversed sorted according to relevant
            # scores even across multiple documents.
            relevant_chunks.sort(key=lambda c: c.chunk_relevance_score, reverse=True)

        return VectorStoreQueryResult(
            nodes=[
                TextNode(
                    text=chunk.chunk.data.string_value,
                    id_=_extract_chunk_id(chunk.chunk.name),
                )
                for chunk in relevant_chunks
            ],
            ids=[_extract_chunk_id(chunk.chunk.name) for chunk in relevant_chunks],
            similarities=[chunk.chunk_relevance_score for chunk in relevant_chunks],
        )
