class TableOutput(BaseModel):
    """Output from analyzing a table."""

    summary: str
    columns: List[TableColumnOutput]
