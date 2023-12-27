class BaseEvaporateProgram(BasePydanticProgram, Generic[Model]):
    """BaseEvaporate program.

    You should provide the fields you want to extract.
    Then when you call the program you should pass in a list of training_data nodes
    and a list of infer_data nodes. The program will call the EvaporateExtractor
    to synthesize a python function from the training data and then apply the function
    to the infer_data.
    """

    def __init__(
        self,
        extractor: EvaporateExtractor,
        fields_to_extract: Optional[List[str]] = None,
        fields_context: Optional[Dict[str, Any]] = None,
        nodes_to_fit: Optional[List[BaseNode]] = None,
        verbose: bool = False,
    ) -> None:
        """Init params."""
        self._extractor = extractor
        self._fields = fields_to_extract or []
        self._fields_context = fields_context or {}
        # NOTE: this will change with each call to `fit`
        self._field_fns: Dict[str, str] = {}
        self._verbose = verbose

        # if nodes_to_fit is not None, then fit extractor
        if nodes_to_fit is not None:
            self._field_fns = self.fit_fields(nodes_to_fit)

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
        """Evaporate program."""
        extractor = EvaporateExtractor(
            service_context=service_context,
            schema_id_prompt=schema_id_prompt,
            fn_generate_prompt=fn_generate_prompt,
            field_extract_query_tmpl=field_extract_query_tmpl,
        )
        return cls(
            extractor,
            fields_to_extract=fields_to_extract,
            fields_context=fields_context,
            nodes_to_fit=nodes_to_fit,
            verbose=verbose,
        )

    @property
    def extractor(self) -> EvaporateExtractor:
        """Extractor."""
        return self._extractor

    def get_function_str(self, field: str) -> str:
        """Get function string."""
        return self._field_fns[field]

    def set_fields_to_extract(self, fields: List[str]) -> None:
        """Set fields to extract."""
        self._fields = fields

    def fit_fields(
        self,
        nodes: List[BaseNode],
        inplace: bool = True,
    ) -> Dict[str, str]:
        """Fit on all fields."""
        if len(self._fields) == 0:
            raise ValueError("Must provide at least one field to extract.")

        field_fns = {}
        for field in self._fields:
            field_context = self._fields_context.get(field, None)
            field_fns[field] = self.fit(
                nodes, field, field_context=field_context, inplace=inplace
            )
        return field_fns

    @abstractmethod
    def fit(
        self,
        nodes: List[BaseNode],
        field: str,
        field_context: Optional[Any] = None,
        expected_output: Optional[Any] = None,
        inplace: bool = True,
    ) -> str:
        """Given the input Nodes and fields, synthesize the python code."""
