def md_to_df(md_str: str) -> pd.DataFrame:
    """Convert Markdown to dataframe."""
    # Replace markdown pipe tables with commas
    md_str = md_str.replace("|", ",")

    # Remove the second line (table header separator)
    lines = md_str.split("\n")
    md_str = "\n".join(lines[:1] + lines[2:])

    # Remove the first and last character (the pipes)
    lines = md_str.split("\n")
    md_str = "\n".join([line[1:-1] for line in lines])

    # Check if the table is empty
    if len(md_str) == 0:
        return None

    # Use pandas to read the CSV string into a DataFrame
    return pd.read_csv(StringIO(md_str))
