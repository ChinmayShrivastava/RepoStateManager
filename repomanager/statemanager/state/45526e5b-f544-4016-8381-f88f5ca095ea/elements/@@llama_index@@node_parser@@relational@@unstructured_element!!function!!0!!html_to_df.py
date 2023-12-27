def html_to_df(html_str: str) -> pd.DataFrame:
    """Convert HTML to dataframe."""
    from lxml import html

    tree = html.fromstring(html_str)
    table_element = tree.xpath("//table")[0]
    rows = table_element.xpath(".//tr")

    data = []
    for row in rows:
        cols = row.xpath(".//td")
        cols = [c.text.strip() if c.text is not None else "" for c in cols]
        data.append(cols)

    # Check if the table is empty
    if len(data) == 0:
        return None

    # Check if the all rows have the same number of columns
    if not all(len(row) == len(data[0]) for row in data):
        return None

    return pd.DataFrame(data[1:], columns=data[0])
