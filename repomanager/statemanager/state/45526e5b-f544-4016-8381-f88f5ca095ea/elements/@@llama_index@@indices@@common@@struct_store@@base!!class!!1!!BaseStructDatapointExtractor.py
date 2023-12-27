class BaseStructDatapointExtractor:
    """Extracts datapoints from a structured document."""

    def __init__(
        self,
        llm: LLMPredictorType,
        schema_extract_prompt: BasePromptTemplate,
        output_parser: OUTPUT_PARSER_TYPE,
    ) -> None:
        """Initialize params."""
        self._llm = llm
        self._schema_extract_prompt = schema_extract_prompt
        self._output_parser = output_parser

    def _clean_and_validate_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fields with col_types_map."""
        new_fields = {}
        col_types_map = self._get_col_types_map()
        for field, value in fields.items():
            clean_value = value
            if field not in col_types_map:
                continue
            # if expected type is int or float, try to convert value to int or float
            expected_type = col_types_map[field]
            if expected_type == int:
                try:
                    clean_value = int(value)
                except ValueError:
                    continue
            elif expected_type == float:
                try:
                    clean_value = float(value)
                except ValueError:
                    continue
            else:
                if len(value) == 0:
                    continue
                if not isinstance(value, col_types_map[field]):
                    continue
            new_fields[field] = clean_value
        return new_fields

    @abstractmethod
    def _insert_datapoint(self, datapoint: StructDatapoint) -> None:
        """Insert datapoint into index."""

    @abstractmethod
    def _get_col_types_map(self) -> Dict[str, type]:
        """Get col types map for schema."""

    @abstractmethod
    def _get_schema_text(self) -> str:
        """Get schema text for extracting relevant info from unstructured text."""

    def insert_datapoint_from_nodes(self, nodes: Sequence[BaseNode]) -> None:
        """Extract datapoint from a document and insert it."""
        text_chunks = [
            node.get_content(metadata_mode=MetadataMode.LLM) for node in nodes
        ]
        fields = {}
        for i, text_chunk in enumerate(text_chunks):
            fmt_text_chunk = truncate_text(text_chunk, 50)
            logger.info(f"> Adding chunk {i}: {fmt_text_chunk}")
            # if embedding specified in document, pass it to the Node
            schema_text = self._get_schema_text()
            response_str = self._llm.predict(
                self._schema_extract_prompt,
                text=text_chunk,
                schema=schema_text,
            )
            cur_fields = self._output_parser(response_str)
            if cur_fields is None:
                continue
            # validate fields with col_types_map
            new_cur_fields = self._clean_and_validate_fields(cur_fields)
            fields.update(new_cur_fields)
        struct_datapoint = StructDatapoint(fields)
        if struct_datapoint is not None:
            self._insert_datapoint(struct_datapoint)
            logger.debug(f"> Added datapoint: {fields}")
