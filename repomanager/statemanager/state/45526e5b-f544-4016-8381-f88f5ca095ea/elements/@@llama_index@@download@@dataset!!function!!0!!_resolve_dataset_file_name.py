def _resolve_dataset_file_name(class_name: str) -> str:
    """Resolve filename based on dataset class."""
    try:
        return DATASET_CLASS_FILENAME_REGISTRY[class_name]
    except KeyError as err:
        raise ValueError("Invalid dataset filename.") from err
