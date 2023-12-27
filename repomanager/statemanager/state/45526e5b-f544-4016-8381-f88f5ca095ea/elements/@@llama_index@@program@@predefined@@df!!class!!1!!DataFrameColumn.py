class DataFrameColumn(BaseModel):
    """Column in a DataFrame."""

    column_name: str = Field(..., description="Column name.")
    column_desc: Optional[str] = Field(..., description="Column description.")
