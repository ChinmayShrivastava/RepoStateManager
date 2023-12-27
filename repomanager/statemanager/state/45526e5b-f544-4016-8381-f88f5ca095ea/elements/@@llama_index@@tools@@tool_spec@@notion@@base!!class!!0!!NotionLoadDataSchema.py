class NotionLoadDataSchema(BaseModel):
    """Notion load data schema."""

    page_ids: Optional[List[str]] = None
    database_id: Optional[str] = None
