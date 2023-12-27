class KnowledgeGraphRAGRetriever(BaseRetriever):
    """
    Knowledge Graph RAG retriever.

    Retriever that perform SubGraph RAG towards knowledge graph.

    Args:
        service_context (Optional[ServiceContext]): A service context to use.
        storage_context (Optional[StorageContext]): A storage context to use.
        entity_extract_fn (Optional[Callable]): A function to extract entities.
        entity_extract_template Optional[BasePromptTemplate]): A Query Key Entity
            Extraction Prompt (see :ref:`Prompt-Templates`).
        entity_extract_policy (Optional[str]): The entity extraction policy to use.
            default: "union"
            possible values: "union", "intersection"
        synonym_expand_fn (Optional[Callable]): A function to expand synonyms.
        synonym_expand_template (Optional[QueryKeywordExpandPrompt]): A Query Key Entity
            Expansion Prompt (see :ref:`Prompt-Templates`).
        synonym_expand_policy (Optional[str]): The synonym expansion policy to use.
            default: "union"
            possible values: "union", "intersection"
        max_entities (int): The maximum number of entities to extract.
            default: 5
        max_synonyms (int): The maximum number of synonyms to expand per entity.
            default: 5
        retriever_mode (Optional[str]): The retriever mode to use.
            default: "keyword"
            possible values: "keyword", "embedding", "keyword_embedding"
        with_nl2graphquery (bool): Whether to combine NL2GraphQuery in context.
            default: False
        graph_traversal_depth (int): The depth of graph traversal.
            default: 2
        max_knowledge_sequence (int): The maximum number of knowledge sequence to
            include in the response. By default, it's 30.
        verbose (bool): Whether to print out debug info.
    """

    def __init__(
        self,
        service_context: Optional[ServiceContext] = None,
        storage_context: Optional[StorageContext] = None,
        entity_extract_fn: Optional[Callable] = None,
        entity_extract_template: Optional[BasePromptTemplate] = None,
        entity_extract_policy: Optional[str] = "union",
        synonym_expand_fn: Optional[Callable] = None,
        synonym_expand_template: Optional[BasePromptTemplate] = None,
        synonym_expand_policy: Optional[str] = "union",
        max_entities: int = 5,
        max_synonyms: int = 5,
        retriever_mode: Optional[str] = "keyword",
        with_nl2graphquery: bool = False,
        graph_traversal_depth: int = 2,
        max_knowledge_sequence: int = REL_TEXT_LIMIT,
        verbose: bool = False,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the retriever."""
        # Ensure that we have a graph store
        assert storage_context is not None, "Must provide a storage context."
        assert (
            storage_context.graph_store is not None
        ), "Must provide a graph store in the storage context."
        self._storage_context = storage_context
        self._graph_store = storage_context.graph_store

        self._service_context = service_context or ServiceContext.from_defaults()

        self._entity_extract_fn = entity_extract_fn
        self._entity_extract_template = (
            entity_extract_template or DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE
        )
        self._entity_extract_policy = entity_extract_policy

        self._synonym_expand_fn = synonym_expand_fn
        self._synonym_expand_template = (
            synonym_expand_template or DEFAULT_SYNONYM_EXPAND_PROMPT
        )
        self._synonym_expand_policy = synonym_expand_policy

        self._max_entities = max_entities
        self._max_synonyms = max_synonyms
        self._retriever_mode = retriever_mode
        self._with_nl2graphquery = with_nl2graphquery
        if self._with_nl2graphquery:
            from llama_index.query_engine.knowledge_graph_query_engine import (
                KnowledgeGraphQueryEngine,
            )

            graph_query_synthesis_prompt = kwargs.get(
                "graph_query_synthesis_prompt",
                None,
            )
            if graph_query_synthesis_prompt is not None:
                del kwargs["graph_query_synthesis_prompt"]

            graph_response_answer_prompt = kwargs.get(
                "graph_response_answer_prompt",
                None,
            )
            if graph_response_answer_prompt is not None:
                del kwargs["graph_response_answer_prompt"]

            refresh_schema = kwargs.get("refresh_schema", False)
            response_synthesizer = kwargs.get("response_synthesizer", None)
            self._kg_query_engine = KnowledgeGraphQueryEngine(
                service_context=self._service_context,
                storage_context=self._storage_context,
                graph_query_synthesis_prompt=graph_query_synthesis_prompt,
                graph_response_answer_prompt=graph_response_answer_prompt,
                refresh_schema=refresh_schema,
                verbose=verbose,
                response_synthesizer=response_synthesizer,
                **kwargs,
            )

        self._graph_traversal_depth = graph_traversal_depth
        self._max_knowledge_sequence = max_knowledge_sequence
        self._verbose = verbose
        refresh_schema = kwargs.get("refresh_schema", False)
        try:
            self._graph_schema = self._graph_store.get_schema(refresh=refresh_schema)
        except NotImplementedError:
            self._graph_schema = ""
        except Exception as e:
            logger.warning(f"Failed to get graph schema: {e}")
            self._graph_schema = ""
        super().__init__(callback_manager)

    def _process_entities(
        self,
        query_str: str,
        handle_fn: Optional[Callable],
        handle_llm_prompt_template: Optional[BasePromptTemplate],
        cross_handle_policy: Optional[str] = "union",
        max_items: Optional[int] = 5,
        result_start_token: str = "KEYWORDS:",
    ) -> List[str]:
        """Get entities from query string."""
        assert cross_handle_policy in [
            "union",
            "intersection",
        ], "Invalid entity extraction policy."
        if cross_handle_policy == "intersection":
            assert all(
                [
                    handle_fn is not None,
                    handle_llm_prompt_template is not None,
                ]
            ), "Must provide entity extract function and template."
        assert any(
            [
                handle_fn is not None,
                handle_llm_prompt_template is not None,
            ]
        ), "Must provide either entity extract function or template."
        enitities_fn: List[str] = []
        enitities_llm: Set[str] = set()

        if handle_fn is not None:
            enitities_fn = handle_fn(query_str)
        if handle_llm_prompt_template is not None:
            response = self._service_context.llm.predict(
                handle_llm_prompt_template,
                max_keywords=max_items,
                question=query_str,
            )
            enitities_llm = extract_keywords_given_response(
                response, start_token=result_start_token, lowercase=False
            )
        if cross_handle_policy == "union":
            entities = list(set(enitities_fn) | enitities_llm)
        elif cross_handle_policy == "intersection":
            entities = list(set(enitities_fn).intersection(set(enitities_llm)))
        if self._verbose:
            print_text(f"Entities processed: {entities}\n", color="green")

        return entities

    async def _aprocess_entities(
        self,
        query_str: str,
        handle_fn: Optional[Callable],
        handle_llm_prompt_template: Optional[BasePromptTemplate],
        cross_handle_policy: Optional[str] = "union",
        max_items: Optional[int] = 5,
        result_start_token: str = "KEYWORDS:",
    ) -> List[str]:
        """Get entities from query string."""
        assert cross_handle_policy in [
            "union",
            "intersection",
        ], "Invalid entity extraction policy."
        if cross_handle_policy == "intersection":
            assert all(
                [
                    handle_fn is not None,
                    handle_llm_prompt_template is not None,
                ]
            ), "Must provide entity extract function and template."
        assert any(
            [
                handle_fn is not None,
                handle_llm_prompt_template is not None,
            ]
        ), "Must provide either entity extract function or template."
        enitities_fn: List[str] = []
        enitities_llm: Set[str] = set()

        if handle_fn is not None:
            enitities_fn = handle_fn(query_str)
        if handle_llm_prompt_template is not None:
            response = await self._service_context.llm.apredict(
                handle_llm_prompt_template,
                max_keywords=max_items,
                question=query_str,
            )
            enitities_llm = extract_keywords_given_response(
                response, start_token=result_start_token, lowercase=False
            )
        if cross_handle_policy == "union":
            entities = list(set(enitities_fn) | enitities_llm)
        elif cross_handle_policy == "intersection":
            entities = list(set(enitities_fn).intersection(set(enitities_llm)))
        if self._verbose:
            print_text(f"Entities processed: {entities}\n", color="green")

        return entities

    def _get_entities(self, query_str: str) -> List[str]:
        """Get entities from query string."""
        entities = self._process_entities(
            query_str,
            self._entity_extract_fn,
            self._entity_extract_template,
            self._entity_extract_policy,
            self._max_entities,
            "KEYWORDS:",
        )
        expanded_entities = self._expand_synonyms(entities)
        return list(set(entities) | set(expanded_entities))

    async def _aget_entities(self, query_str: str) -> List[str]:
        """Get entities from query string."""
        entities = await self._aprocess_entities(
            query_str,
            self._entity_extract_fn,
            self._entity_extract_template,
            self._entity_extract_policy,
            self._max_entities,
            "KEYWORDS:",
        )
        expanded_entities = await self._aexpand_synonyms(entities)
        return list(set(entities) | set(expanded_entities))

    def _expand_synonyms(self, keywords: List[str]) -> List[str]:
        """Expand synonyms or similar expressions for keywords."""
        return self._process_entities(
            str(keywords),
            self._synonym_expand_fn,
            self._synonym_expand_template,
            self._synonym_expand_policy,
            self._max_synonyms,
            "SYNONYMS:",
        )

    async def _aexpand_synonyms(self, keywords: List[str]) -> List[str]:
        """Expand synonyms or similar expressions for keywords."""
        return await self._aprocess_entities(
            str(keywords),
            self._synonym_expand_fn,
            self._synonym_expand_template,
            self._synonym_expand_policy,
            self._max_synonyms,
            "SYNONYMS:",
        )

    def _get_knowledge_sequence(
        self, entities: List[str]
    ) -> Tuple[List[str], Optional[Dict[Any, Any]]]:
        """Get knowledge sequence from entities."""
        # Get SubGraph from Graph Store as Knowledge Sequence
        rel_map: Optional[Dict] = self._graph_store.get_rel_map(
            entities, self._graph_traversal_depth, limit=self._max_knowledge_sequence
        )
        logger.debug(f"rel_map: {rel_map}")

        # Build Knowledge Sequence
        knowledge_sequence = []
        if rel_map:
            knowledge_sequence.extend(
                [str(rel_obj) for rel_objs in rel_map.values() for rel_obj in rel_objs]
            )
        else:
            logger.info("> No knowledge sequence extracted from entities.")
            return [], None

        return knowledge_sequence, rel_map

    async def _aget_knowledge_sequence(
        self, entities: List[str]
    ) -> Tuple[List[str], Optional[Dict[Any, Any]]]:
        """Get knowledge sequence from entities."""
        # Get SubGraph from Graph Store as Knowledge Sequence
        # TBD: async in graph store
        rel_map: Optional[Dict] = self._graph_store.get_rel_map(
            entities, self._graph_traversal_depth, limit=self._max_knowledge_sequence
        )
        logger.debug(f"rel_map from GraphStore:\n{rel_map}")

        # Build Knowledge Sequence
        knowledge_sequence = []
        if rel_map:
            knowledge_sequence.extend(
                [str(rel_obj) for rel_objs in rel_map.values() for rel_obj in rel_objs]
            )
        else:
            logger.info("> No knowledge sequence extracted from entities.")
            return [], None

        return knowledge_sequence, rel_map

    def _build_nodes(
        self, knowledge_sequence: List[str], rel_map: Optional[Dict[Any, Any]] = None
    ) -> List[NodeWithScore]:
        """Build nodes from knowledge sequence."""
        if len(knowledge_sequence) == 0:
            logger.info("> No knowledge sequence extracted from entities.")
            return []
        _new_line_char = "\n"
        context_string = (
            f"The following are knowledge sequence in max depth"
            f" {self._graph_traversal_depth} "
            f"in the form of directed graph like:\n"
            f"`subject -[predicate]->, object, <-[predicate_next_hop]-,"
            f" object_next_hop ...`"
            f" extracted based on key entities as subject:\n"
            f"{_new_line_char.join(knowledge_sequence)}"
        )
        if self._verbose:
            print_text(f"Graph RAG context:\n{context_string}\n", color="blue")

        rel_node_info = {
            "kg_rel_map": rel_map,
            "kg_rel_text": knowledge_sequence,
        }
        metadata_keys = ["kg_rel_map", "kg_rel_text"]
        if self._graph_schema != "":
            rel_node_info["kg_schema"] = {"schema": self._graph_schema}
            metadata_keys.append("kg_schema")
        node = NodeWithScore(
            node=TextNode(
                text=context_string,
                score=1.0,
                metadata=rel_node_info,
                excluded_embed_metadata_keys=metadata_keys,
                excluded_llm_metadata_keys=metadata_keys,
            )
        )
        return [node]

    def _retrieve_keyword(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve in keyword mode."""
        if self._retriever_mode not in ["keyword", "keyword_embedding"]:
            return []
        # Get entities
        entities = self._get_entities(query_bundle.query_str)
        # Before we enable embedding/semantic search, we need to make sure
        # we don't miss any entities that's synoynm of the entities we extracted
        # in string matching based retrieval in following steps, thus we expand
        # synonyms here.
        if len(entities) == 0:
            logger.info("> No entities extracted from query string.")
            return []

        # Get SubGraph from Graph Store as Knowledge Sequence
        knowledge_sequence, rel_map = self._get_knowledge_sequence(entities)

        return self._build_nodes(knowledge_sequence, rel_map)

    async def _aretrieve_keyword(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        """Retrieve in keyword mode."""
        if self._retriever_mode not in ["keyword", "keyword_embedding"]:
            return []
        # Get entities
        entities = await self._aget_entities(query_bundle.query_str)
        # Before we enable embedding/semantic search, we need to make sure
        # we don't miss any entities that's synoynm of the entities we extracted
        # in string matching based retrieval in following steps, thus we expand
        # synonyms here.
        if len(entities) == 0:
            logger.info("> No entities extracted from query string.")
            return []

        # Get SubGraph from Graph Store as Knowledge Sequence
        knowledge_sequence, rel_map = await self._aget_knowledge_sequence(entities)

        return self._build_nodes(knowledge_sequence, rel_map)

    def _retrieve_embedding(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve in embedding mode."""
        if self._retriever_mode not in ["embedding", "keyword_embedding"]:
            return []
        # TBD: will implement this later with vector store.
        raise NotImplementedError

    async def _aretrieve_embedding(
        self, query_bundle: QueryBundle
    ) -> List[NodeWithScore]:
        """Retrieve in embedding mode."""
        if self._retriever_mode not in ["embedding", "keyword_embedding"]:
            return []
        # TBD: will implement this later with vector store.
        raise NotImplementedError

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Build nodes for response."""
        nodes: List[NodeWithScore] = []
        if self._with_nl2graphquery:
            try:
                nodes_nl2graphquery = self._kg_query_engine._retrieve(query_bundle)
                nodes.extend(nodes_nl2graphquery)
            except Exception as e:
                logger.warning(f"Error in retrieving from nl2graphquery: {e}")

        nodes.extend(self._retrieve_keyword(query_bundle))
        nodes.extend(self._retrieve_embedding(query_bundle))

        return nodes

    async def _aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Build nodes for response."""
        nodes: List[NodeWithScore] = []
        if self._with_nl2graphquery:
            try:
                nodes_nl2graphquery = await self._kg_query_engine._aretrieve(
                    query_bundle
                )
                nodes.extend(nodes_nl2graphquery)
            except Exception as e:
                logger.warning(f"Error in retrieving from nl2graphquery: {e}")

        nodes.extend(await self._aretrieve_keyword(query_bundle))
        nodes.extend(await self._aretrieve_embedding(query_bundle))

        return nodes