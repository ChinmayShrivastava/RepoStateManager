class ReaderConfig(BaseComponent):
    """Represents a reader and it's input arguments."""

    reader: BasePydanticReader = Field(..., description="Reader to use.")
    reader_args: List[Any] = Field(default_factory=list, description="Reader args.")
    reader_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Reader kwargs."
    )

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def class_name(cls) -> str:
        """Get the name identifier of the class."""
        return "ReaderConfig"

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        """Convert the class to a dictionary."""
        return {
            "loader": self.reader.to_dict(**kwargs),
            "reader_args": self.reader_args,
            "reader_kwargs": self.reader_kwargs,
            "class_name": self.class_name(),
        }

    def read(self) -> List[Document]:
        """Call the loader with the given arguments."""
        return self.reader.load_data(*self.reader_args, **self.reader_kwargs)
