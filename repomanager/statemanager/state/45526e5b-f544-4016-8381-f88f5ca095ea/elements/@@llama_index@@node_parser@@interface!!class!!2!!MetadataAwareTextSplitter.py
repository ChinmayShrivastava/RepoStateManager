class MetadataAwareTextSplitter(TextSplitter):
    @abstractmethod
    def split_text_metadata_aware(self, text: str, metadata_str: str) -> List[str]:
        ...

    def split_texts_metadata_aware(
        self, texts: List[str], metadata_strs: List[str]
    ) -> List[str]:
        if len(texts) != len(metadata_strs):
            raise ValueError("Texts and metadata_strs must have the same length")
        nested_texts = [
            self.split_text_metadata_aware(text, metadata)
            for text, metadata in zip(texts, metadata_strs)
        ]
        return [item for sublist in nested_texts for item in sublist]

    def _get_metadata_str(self, node: BaseNode) -> str:
        """Helper function to get the proper metadata str for splitting."""
        embed_metadata_str = node.get_metadata_str(mode=MetadataMode.EMBED)
        llm_metadata_str = node.get_metadata_str(mode=MetadataMode.LLM)

        # use the longest metadata str for splitting
        if len(embed_metadata_str) > len(llm_metadata_str):
            metadata_str = embed_metadata_str
        else:
            metadata_str = llm_metadata_str

        return metadata_str

    def _parse_nodes(
        self, nodes: Sequence[BaseNode], show_progress: bool = False, **kwargs: Any
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")

        for node in nodes_with_progress:
            metadata_str = self._get_metadata_str(node)
            splits = self.split_text_metadata_aware(
                node.get_content(metadata_mode=MetadataMode.NONE),
                metadata_str=metadata_str,
            )
            all_nodes.extend(
                build_nodes_from_splits(splits, node, id_func=self.id_func)
            )

        return all_nodes
