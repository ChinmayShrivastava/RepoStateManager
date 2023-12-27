def _resolve_dataset_class(filename: str) -> Type[BaseLlamaDataset]:
    """Resolve appropriate llama dataset class based on file name."""
    if "rag_dataset.json" in filename:
        return LabelledRagDataset
    elif "pairwise_evaluator_dataset.json" in filename:
        return LabelledPairwiseEvaluatorDataset
    elif "evaluator_dataset.json" in filename:
        return LabelledEvaluatorDataset
    else:
        raise ValueError("Unknown filename.")
