class DataFrameRow(BaseModel):
    """Row in a DataFrame."""

    row_values: List[Any] = Field(
        ...,
        description="List of row values, where each value corresponds to a row key.",
    )
