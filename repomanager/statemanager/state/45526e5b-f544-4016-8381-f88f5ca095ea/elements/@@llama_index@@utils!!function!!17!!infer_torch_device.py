def infer_torch_device() -> str:
    """Infer the input to torch.device."""
    try:
        has_cuda = torch.cuda.is_available()
    except NameError:
        import torch

        has_cuda = torch.cuda.is_available()
    if has_cuda:
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"
