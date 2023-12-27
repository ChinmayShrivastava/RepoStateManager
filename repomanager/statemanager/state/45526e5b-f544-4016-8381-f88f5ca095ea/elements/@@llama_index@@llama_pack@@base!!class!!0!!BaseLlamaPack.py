class BaseLlamaPack:
    @abstractmethod
    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run."""
