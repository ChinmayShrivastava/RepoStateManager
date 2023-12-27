class BaseObjectNodeMapping(Generic[OT]):
    """Base object node mapping."""

    @classmethod
    @abstractmethod
    def from_objects(
        cls, objs: Sequence[OT], *args: Any, **kwargs: Any
    ) -> "BaseObjectNodeMapping":
        """Initialize node mapping from a list of objects.

        Only needs to be specified if the node mapping
        needs to be initialized with a list of objects.

        """

    def validate_object(self, obj: OT) -> None:
        """Validate object."""

    def add_object(self, obj: OT) -> None:
        """Add object.

        Only needs to be specified if the node mapping
        needs to be initialized with a list of objects.

        """
        self.validate_object(obj)
        self._add_object(obj)

    @property
    @abstractmethod
    def obj_node_mapping(self) -> Dict[Any, Any]:
        """The mapping data structure between node and object."""

    @abstractmethod
    def _add_object(self, obj: OT) -> None:
        """Add object.

        Only needs to be specified if the node mapping
        needs to be initialized with a list of objects.

        """

    @abstractmethod
    def to_node(self, obj: OT) -> TextNode:
        """To node."""

    def to_nodes(self, objs: Sequence[OT]) -> Sequence[TextNode]:
        return [self.to_node(obj) for obj in objs]

    def from_node(self, node: BaseNode) -> OT:
        """From node."""
        obj = self._from_node(node)
        self.validate_object(obj)
        return obj

    @abstractmethod
    def _from_node(self, node: BaseNode) -> OT:
        """From node."""

    @abstractmethod
    def persist(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> None:
        """Persist objs."""

    @classmethod
    def from_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> "BaseObjectNodeMapping[OT]":
        """Load from serialization."""
        obj_node_mapping = None
        errors = []
        for cls in BaseObjectNodeMapping.__subclasses__():  # type: ignore[misc]
            try:
                obj_node_mapping = cls.from_persist_dir(
                    persist_dir=persist_dir,
                    obj_node_mapping_fname=obj_node_mapping_fname,
                )
                break
            except (NotImplementedError, pickle.PickleError) as err:
                # raise unhandled exception otherwise
                errors.append(err)
        if obj_node_mapping:
            return obj_node_mapping
        else:
            raise Exception(errors)
