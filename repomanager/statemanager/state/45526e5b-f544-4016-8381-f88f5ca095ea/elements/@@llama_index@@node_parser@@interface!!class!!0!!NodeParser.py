class NodeParser(TransformComponent, ABC):
    """Base interface for node parser."""

    include_metadata: bool = Field(
        default=True, description="Whether or not to consider metadata when splitting."
    )
    include_prev_next_rel: bool = Field(
        default=True, description="Include prev/next node relationships."
    )
    callback_manager: CallbackManager = Field(
        default_factory=CallbackManager, exclude=True
    )
    id_func: IdFuncCallable = Field(
        default=default_id_func,
        description="Function to generate node IDs.",
    )

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        ...

    def get_nodes_from_documents(
        self,
        documents: Sequence[Document],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        """Parse documents into nodes.

        Args:
            documents (Sequence[Document]): documents to parse
            show_progress (bool): whether to show progress bar

        """
        doc_id_to_document = {doc.id_: doc for doc in documents}

        with self.callback_manager.event(
            CBEventType.NODE_PARSING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            nodes = self._parse_nodes(documents, show_progress=show_progress, **kwargs)

            for i, node in enumerate(nodes):
                if (
                    node.ref_doc_id is not None
                    and node.ref_doc_id in doc_id_to_document
                ):
                    ref_doc = doc_id_to_document[node.ref_doc_id]
                    start_char_idx = ref_doc.text.find(
                        node.get_content(metadata_mode=MetadataMode.NONE)
                    )

                    # update start/end char idx
                    if start_char_idx >= 0:
                        node.start_char_idx = start_char_idx
                        node.end_char_idx = start_char_idx + len(
                            node.get_content(metadata_mode=MetadataMode.NONE)
                        )

                    # update metadata
                    if self.include_metadata:
                        node.metadata.update(
                            doc_id_to_document[node.ref_doc_id].metadata
                        )

                if self.include_prev_next_rel:
                    if i > 0:
                        node.relationships[NodeRelationship.PREVIOUS] = nodes[
                            i - 1
                        ].as_related_node_info()
                    if i < len(nodes) - 1:
                        node.relationships[NodeRelationship.NEXT] = nodes[
                            i + 1
                        ].as_related_node_info()

            event.on_end({EventPayload.NODES: nodes})

        return nodes

    def __call__(self, nodes: List[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return self.get_nodes_from_documents(nodes, **kwargs)
