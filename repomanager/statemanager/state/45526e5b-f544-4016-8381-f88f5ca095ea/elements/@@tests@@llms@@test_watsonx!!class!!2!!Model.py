    class Model:
        def __init__(
            self,
            model_id: str,
            credentials: dict,
            project_id: Optional[str] = None,
            space_id: Optional[str] = None,
        ) -> None:
            pass

        def get_details(self) -> Dict[str, Any]:
            return {"model_details": "Mock IBM Watson Model"}

        def generate_text(self, prompt: str, params: Optional[dict] = None) -> str:
            return "\n\nThis is indeed a test"

        def generate_text_stream(
            self, prompt: str, params: Optional[dict] = None
        ) -> MockStreamResponse:
            return MockStreamResponse()
