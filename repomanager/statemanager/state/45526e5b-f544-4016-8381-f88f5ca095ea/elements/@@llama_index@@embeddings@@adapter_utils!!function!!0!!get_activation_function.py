def get_activation_function(name: str) -> Callable:
    """Get activation function.

    Args:
        name (str): Name of activation function.

    """
    activations: Dict[str, Callable] = {
        "relu": F.relu,
        "sigmoid": torch.sigmoid,
        "tanh": torch.tanh,
        "leaky_relu": F.leaky_relu,
        # add more activations here as needed
    }
    if name not in activations:
        raise ValueError(f"Unknown activation function: {name}")
    return activations[name]
