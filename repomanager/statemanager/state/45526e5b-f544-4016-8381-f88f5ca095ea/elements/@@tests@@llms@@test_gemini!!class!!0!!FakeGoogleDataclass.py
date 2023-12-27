class FakeGoogleDataclass(types.SimpleNamespace):
    """Emulate the dataclasses used in the genai package."""

    def __init__(self, d: Mapping[str, Any], *args: Any, **kwargs: Any):
        self.d = d
        super().__init__(**d)

    def to_dict(self) -> Mapping[str, Any]:
        return self.d
