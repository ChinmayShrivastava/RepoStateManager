class DataFrameRowsOnly(BaseModel):
    """Data-frame with rows. Assume column names are already known beforehand."""

    rows: List[DataFrameRow] = Field(..., description="""List of row objects.""")

    def to_df(self, existing_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """To dataframe."""
        if existing_df is None:
            return pd.DataFrame([row.row_values for row in self.rows])
        else:
            new_df = pd.DataFrame([row.row_values for row in self.rows])
            new_df.columns = existing_df.columns
            # assume row values are in order of column names
            return existing_df.append(new_df, ignore_index=True)
