class SQLTableSchema(BaseModel):
    """Lightweight representation of a SQL table."""

    table_name: str
    context_str: Optional[str] = None
