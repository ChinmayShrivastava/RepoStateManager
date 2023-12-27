def as_dataframe(data: Iterable[BaseDataType]) -> "DataFrame":
    """Converts a list of BaseDataType to a pandas dataframe.

    Args:
        data (Iterable[BaseDataType]): A list of BaseDataType.

    Returns:
        DataFrame: The converted pandas dataframe.
    """
    pandas = _import_package("pandas")
    as_dict_list = []
    for datum in data:
        as_dict = {
            field.metadata.get(OPENINFERENCE_COLUMN_NAME, field.name): getattr(
                datum, field.name
            )
            for field in fields(datum)
        }
        as_dict_list.append(as_dict)

    return pandas.DataFrame(as_dict_list)
