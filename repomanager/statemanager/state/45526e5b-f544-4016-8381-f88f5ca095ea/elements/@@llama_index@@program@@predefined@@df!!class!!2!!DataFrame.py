class DataFrame(BaseModel):
    """Data-frame class.

    Consists of a `rows` field which is a list of dictionaries,
    as well as a `columns` field which is a list of column names.

    """

    description: Optional[str] = None

    columns: List[DataFrameColumn] = Field(..., description="List of column names.")
    rows: List[DataFrameRow] = Field(
        ...,
        description="""List of DataFrameRow objects. Each DataFrameRow contains \
        valuesin order of the data frame column.""",
    )

    def to_df(self) -> pd.DataFrame:
        """To dataframe."""
        return pd.DataFrame(
            [row.row_values for row in self.rows],
            columns=[col.column_name for col in self.columns],
        )
