class BasePydanticReader(BaseReader, BaseComponent):
    """Serialiable Data Loader with Pydatnic."""

    is_remote: bool = Field(
        default=False,
        description="Whether the data is loaded from a remote API or a local file.",
    )

    class Config:
        arbitrary_types_allowed = True
