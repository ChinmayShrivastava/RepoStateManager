class DataFrameValuesPerColumn(BaseModel):
    """Data-frame as a list of column objects.

    Each column object contains a list of values. Note that they can be
    of variable length, and so may not be able to be converted to a dataframe.

    """

    columns: List[DataFrameRow] = Field(..., description="""List of column objects.""")
