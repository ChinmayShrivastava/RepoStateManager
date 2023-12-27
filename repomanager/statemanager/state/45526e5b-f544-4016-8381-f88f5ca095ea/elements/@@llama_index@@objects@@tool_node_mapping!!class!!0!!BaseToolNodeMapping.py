class BaseToolNodeMapping(BaseObjectNodeMapping[BaseTool]):
    """Base Tool node mapping."""

    def validate_object(self, obj: BaseTool) -> None:
        if not isinstance(obj, BaseTool):
            raise ValueError(f"Object must be of type {BaseTool}")

    @property
    def obj_node_mapping(self) -> Dict[int, Any]:
        """The mapping data structure between node and object."""
        raise NotImplementedError("Subclasses should implement this!")

    def persist(
        self, persist_dir: str = ..., obj_node_mapping_fname: str = ...
    ) -> None:
        """Persist objs."""
        raise NotImplementedError("Subclasses should implement this!")

    @classmethod
    def from_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> "BaseToolNodeMapping":
        raise NotImplementedError(
            "This object node mapping does not support persist method."
        )
