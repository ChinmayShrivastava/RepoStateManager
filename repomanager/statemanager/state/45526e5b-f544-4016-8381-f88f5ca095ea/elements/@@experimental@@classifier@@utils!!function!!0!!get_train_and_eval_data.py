def get_train_and_eval_data(
    csv_path: str,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Get train and eval data."""
    df = pd.read_csv(csv_path)
    label_col = "Survived"
    cols_to_drop = ["PassengerId", "Ticket", "Name", "Cabin"]
    df = df.drop(cols_to_drop, axis=1)
    labels = df.pop(label_col)
    train_df, eval_df, train_labels, eval_labels = train_test_split(
        df, labels, test_size=0.25, random_state=0
    )
    return train_df, train_labels, eval_df, eval_labels
