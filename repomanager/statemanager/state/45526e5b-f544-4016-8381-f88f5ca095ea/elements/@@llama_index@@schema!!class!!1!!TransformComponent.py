class TransformComponent(BaseComponent):
    """Base class for transform components."""

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def __call__(self, nodes: List["BaseNode"], **kwargs: Any) -> List["BaseNode"]:
        """Transform nodes."""

    async def acall(self, nodes: List["BaseNode"], **kwargs: Any) -> List["BaseNode"]:
        """Async transform nodes."""
        return self.__call__(nodes, **kwargs)
