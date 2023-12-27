def get_label_str(labels: pd.Series, i: int) -> str:
    """Get label string."""
    return f"{labels.name}: {labels.iloc[i]}"
