class PIINodePostprocessor(BaseNodePostprocessor):
    """PII Node processor.

    NOTE: the ServiceContext should contain a LOCAL model, not an external API.

    NOTE: this is a beta feature, the API might change.

    Args:
        service_context (ServiceContext): Service context.

    """

    service_context: ServiceContext
    pii_str_tmpl: str = DEFAULT_PII_TMPL
    pii_node_info_key: str = "__pii_node_info__"

    @classmethod
    def class_name(cls) -> str:
        return "PIINodePostprocessor"

    def mask_pii(self, text: str) -> Tuple[str, Dict]:
        """Mask PII in text."""
        pii_prompt = PromptTemplate(self.pii_str_tmpl)
        # TODO: allow customization
        task_str = (
            "Mask out the PII, replace each PII with a tag, and return the text. "
            "Return the mapping in JSON."
        )

        response = self.service_context.llm.predict(
            pii_prompt, context_str=text, query_str=task_str
        )
        splits = response.split("Output Mapping:")
        text_output = splits[0].strip()
        json_str_output = splits[1].strip()
        json_dict = json.loads(json_str_output)
        return text_output, json_dict

    def _postprocess_nodes(
        self,
        nodes: List[NodeWithScore],
        query_bundle: Optional[QueryBundle] = None,
    ) -> List[NodeWithScore]:
        """Postprocess nodes."""
        # swap out text from nodes, with the original node mappings
        new_nodes = []
        for node_with_score in nodes:
            node = node_with_score.node
            new_text, mapping_info = self.mask_pii(
                node.get_content(metadata_mode=MetadataMode.LLM)
            )
            new_node = deepcopy(node)
            new_node.excluded_embed_metadata_keys.append(self.pii_node_info_key)
            new_node.excluded_llm_metadata_keys.append(self.pii_node_info_key)
            new_node.metadata[self.pii_node_info_key] = mapping_info
            new_node.set_content(new_text)
            new_nodes.append(NodeWithScore(node=new_node, score=node_with_score.score))

        return new_nodes
