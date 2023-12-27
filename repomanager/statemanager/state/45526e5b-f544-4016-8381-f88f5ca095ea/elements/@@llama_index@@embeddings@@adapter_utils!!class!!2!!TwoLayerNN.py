class TwoLayerNN(BaseAdapter):
    """Two-layer transformation.

    Args:
        in_features (int): Input dimension.
        hidden_features (int): Hidden dimension.
        out_features (int): Output dimension.
        bias (bool): Whether to use bias. Defaults to False.
        activation_fn_str (str): Name of activation function. Defaults to "relu".

    """

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        out_features: int,
        bias: bool = False,
        activation_fn_str: str = "relu",
        add_residual: bool = False,
    ) -> None:
        super().__init__()
        self.in_features = in_features
        self.hidden_features = hidden_features
        self.out_features = out_features
        self.bias = bias
        self.activation_fn_str = activation_fn_str

        self.linear1 = nn.Linear(in_features, hidden_features, bias=True)
        self.linear2 = nn.Linear(hidden_features, out_features, bias=True)
        # self.linear1.weight.data.copy_(torch.zeros(hidden_features, in_features))
        # self.linear2.weight.data.copy_(torch.zeros(out_features, hidden_features))
        # if bias:
        #     self.linear1.bias.data.copy_(torch.zeros(hidden_features))
        #     self.linear2.bias.data.copy_(torch.zeros(out_features))

        self._activation_function = get_activation_function(activation_fn_str)
        self._add_residual = add_residual
        # if add_residual, then add residual_weight (init to 0)
        self.residual_weight = nn.Parameter(torch.zeros(1))

    def forward(self, embed: Tensor) -> Tensor:
        """Forward pass (Wv).

        Args:
            embed (Tensor): Input tensor.

        """
        output1 = self.linear1(embed)
        output1 = self._activation_function(output1)
        output2 = self.linear2(output1)

        if self._add_residual:
            # print(output2)
            # print(self.residual_weight)
            # print(self.linear2.weight.data)
            output2 = self.residual_weight * output2 + embed

        return output2

    def get_config_dict(self) -> Dict:
        """Get config dict."""
        return {
            "in_features": self.in_features,
            "hidden_features": self.hidden_features,
            "out_features": self.out_features,
            "bias": self.bias,
            "activation_fn_str": self.activation_fn_str,
            "add_residual": self._add_residual,
        }
