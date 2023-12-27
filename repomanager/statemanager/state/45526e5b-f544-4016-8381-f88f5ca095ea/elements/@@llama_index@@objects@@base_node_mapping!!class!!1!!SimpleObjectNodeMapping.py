class SimpleObjectNodeMapping(BaseObjectNodeMapping[Any]):
    """General node mapping that works for any obj.

    More specifically, any object with a meaningful string representation.

    """

    def __init__(self, objs: Optional[Sequence[Any]] = None) -> None:
        objs = objs or []
        for obj in objs:
            self.validate_object(obj)
        self._objs = {hash(str(obj)): obj for obj in objs}

    @classmethod
    def from_objects(
        cls, objs: Sequence[Any], *args: Any, **kwargs: Any
    ) -> "SimpleObjectNodeMapping":
        return cls(objs)

    @property
    def obj_node_mapping(self) -> Dict[int, Any]:
        return self._objs

    @obj_node_mapping.setter
    def obj_node_mapping(self, mapping: Dict[int, Any]) -> None:
        self._objs = mapping

    def _add_object(self, obj: Any) -> None:
        self._objs[hash(str(obj))] = obj

    def to_node(self, obj: Any) -> TextNode:
        return TextNode(text=str(obj))

    def _from_node(self, node: BaseNode) -> Any:
        return self._objs[hash(node.get_content(metadata_mode=MetadataMode.NONE))]

    def persist(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> None:
        """Persist object node mapping.

        NOTE: This may fail depending on whether the object types are
        pickle-able.
        """
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
        obj_node_mapping_path = concat_dirs(persist_dir, obj_node_mapping_fname)
        try:
            with open(obj_node_mapping_path, "wb") as f:
                pickle.dump(self, f)
        except pickle.PickleError as err:
            raise ValueError("Objs is not pickleable") from err

    @classmethod
    def from_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        obj_node_mapping_fname: str = DEFAULT_PERSIST_FNAME,
    ) -> "SimpleObjectNodeMapping":
        obj_node_mapping_path = concat_dirs(persist_dir, obj_node_mapping_fname)
        try:
            with open(obj_node_mapping_path, "rb") as f:
                simple_object_node_mapping = pickle.load(f)
        except pickle.PickleError as err:
            raise ValueError("Objs cannot be loaded.") from err
        return simple_object_node_mapping
