class NotionSearchDataSchema(BaseModel):
    """Notion search data schema."""

    query: str
    direction: Optional[str] = None
    timestamp: Optional[str] = None
    value: Optional[str] = None
    property: Optional[str] = None
    page_size: int = 100
