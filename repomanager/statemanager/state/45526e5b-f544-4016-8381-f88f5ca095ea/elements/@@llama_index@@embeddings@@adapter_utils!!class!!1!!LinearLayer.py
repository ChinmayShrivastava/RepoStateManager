class LinearLayer(BaseAdapter):
    """Linear transformation.

    Args:
        in_features (int): Input dimension.
        out_features (int): Output dimension.
        bias (bool): Whether to use bias. Defaults to False.

    """

    def __init__(self, in_features: int, out_features: int, bias: bool = False) -> None:
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
        self.linear = nn.Linear(in_features, out_features, bias=bias)
        # seed with identity matrix and 0 bias
        # only works for square matrices
        self.linear.weight.data.copy_(torch.eye(in_features, out_features))
        if bias:
            self.linear.bias.data.copy_(torch.zeros(out_features))

    def forward(self, embed: Tensor) -> Tensor:
        """Forward pass (Wv)."""
        return self.linear(embed)

    def get_config_dict(self) -> Dict:
        return {
            "in_features": self.in_features,
            "out_features": self.out_features,
            "bias": self.bias,
        }
