def get_train_str(
    train_df: pd.DataFrame, train_labels: pd.Series, train_n: int = 10
) -> str:
    """Get train str."""
    dict_list = train_df.to_dict("records")[:train_n]
    item_list = []
    for i, d in enumerate(dict_list):
        dict_str = get_sorted_dict_str(d)
        label_str = get_label_str(train_labels, i)
        item_str = (
            f"This is the Data:\n{dict_str}\nThis is the correct answer:\n{label_str}"
        )
        item_list.append(item_str)

    return "\n\n".join(item_list)
