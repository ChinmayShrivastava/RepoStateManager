class BaseAdapter(nn.Module):
    """Base adapter.

    Can be subclassed to implement custom adapters.
    To implement a custom adapter, subclass this class and implement the
    following methods:
        - get_config_dict
        - forward

    """

    @abstractmethod
    def get_config_dict(self) -> Dict:
        """Get config dict."""

    @abstractmethod
    def forward(self, embed: Tensor) -> Tensor:
        """Forward pass."""

    def save(self, output_path: str) -> None:
        """Save model."""
        os.makedirs(output_path, exist_ok=True)
        with open(os.path.join(output_path, "config.json"), "w") as fOut:
            json.dump(self.get_config_dict(), fOut)
        torch.save(self.state_dict(), os.path.join(output_path, "pytorch_model.bin"))

    @classmethod
    def load(cls, input_path: str) -> "BaseAdapter":
        """Load model."""
        with open(os.path.join(input_path, "config.json")) as fIn:
            config = json.load(fIn)
        model = cls(**config)
        model.load_state_dict(
            torch.load(
                os.path.join(input_path, "pytorch_model.bin"),
                map_location=torch.device("cpu"),
            )
        )
        return model
