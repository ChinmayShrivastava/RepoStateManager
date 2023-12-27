class IndexToolConfig(BaseModel):
    """Configuration for LlamaIndex index tool."""

    query_engine: BaseQueryEngine
    name: str
    description: str
    tool_kwargs: Dict = Field(default_factory=dict)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
