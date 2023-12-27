class MultiValueEvaporateProgram(BaseEvaporateProgram[DataFrameValuesPerColumn]):
    """Multi-Value Evaporate program.

    Given a set of fields, and texts extracts a list of `DataFrameRow` objects across
    that texts.
    Each DataFrameRow corresponds to a field, and each value in the row corresponds to
    a value for the field.

    Difference with DFEvaporateProgram is that 1) each DataFrameRow
    is column-oriented (instead of row-oriented), and 2)
    each DataFrameRow can be variable length (not guaranteed to have 1 value per
    node).

    """

    @classmethod
    def from_defaults(
        cls,
        fields_to_extract: Optional[List[str]] = None,
        fields_context: Optional[Dict[str, Any]] = None,
        service_context: Optional[ServiceContext] = None,
        schema_id_prompt: Optional[SchemaIDPrompt] = None,
        fn_generate_prompt: Optional[FnGeneratePrompt] = None,
        field_extract_query_tmpl: str = DEFAULT_FIELD_EXTRACT_QUERY_TMPL,
        nodes_to_fit: Optional[List[BaseNode]] = None,
        verbose: bool = False,
    ) -> "BaseEvaporateProgram":
        # modify the default function generate prompt to return a list
        fn_generate_prompt = fn_generate_prompt or FN_GENERATION_LIST_PROMPT
        return super().from_defaults(
            fields_to_extract=fields_to_extract,
            fields_context=fields_context,
            service_context=service_context,
            schema_id_prompt=schema_id_prompt,
            fn_generate_prompt=fn_generate_prompt,
            field_extract_query_tmpl=field_extract_query_tmpl,
            nodes_to_fit=nodes_to_fit,
            verbose=verbose,
        )

    def fit(
        self,
        nodes: List[BaseNode],
        field: str,
        field_context: Optional[Any] = None,
        expected_output: Optional[Any] = None,
        inplace: bool = True,
    ) -> str:
        """Given the input Nodes and fields, synthesize the python code."""
        fn = self._extractor.extract_fn_from_nodes(
            nodes, field, expected_output=expected_output
        )
        logger.debug(f"Extracted function: {fn}")
        if self._verbose:
            print_text(f"Extracted function: {fn}\n", color="blue")
        if inplace:
            self._field_fns[field] = fn
        return fn

    @property
    def output_cls(self) -> Type[DataFrameValuesPerColumn]:
        """Output class."""
        return DataFrameValuesPerColumn

    def _inference(
        self, nodes: List[BaseNode], fn_str: str, field_name: str
    ) -> List[Any]:
        """Given the input, call the python code and return the result."""
        results_by_node = self._extractor.run_fn_on_nodes(nodes, fn_str, field_name)
        # flatten results
        return [r for results in results_by_node for r in results]

    def __call__(self, *args: Any, **kwds: Any) -> DataFrameValuesPerColumn:
        """Call evaporate on inference data."""
        # TODO: either specify `nodes` or `texts` in kwds
        if "nodes" in kwds:
            nodes = kwds["nodes"]
        elif "texts" in kwds:
            nodes = [TextNode(text=t) for t in kwds["texts"]]
        else:
            raise ValueError("Must provide either `nodes` or `texts`.")

        col_dict = {}
        for field in self._fields:
            col_dict[field] = self._inference(nodes, self._field_fns[field], field)

        # convert col_dict to list of DataFrameRow objects
        df_row_objs = []
        for field in self._fields:
            df_row_objs.append(DataFrameRow(row_values=col_dict[field]))

        return DataFrameValuesPerColumn(columns=df_row_objs)
