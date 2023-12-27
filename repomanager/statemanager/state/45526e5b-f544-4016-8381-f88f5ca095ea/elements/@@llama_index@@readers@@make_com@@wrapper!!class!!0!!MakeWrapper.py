class MakeWrapper(BaseReader):
    """Make reader."""

    def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory.

        NOTE: This is not implemented.

        """
        raise NotImplementedError("Cannot load documents from Make.com API.")

    def pass_response_to_webhook(
        self, webhook_url: str, response: Response, query: Optional[str] = None
    ) -> None:
        """Pass response object to webhook.

        Args:
            webhook_url (str): Webhook URL.
            response (Response): Response object.
            query (Optional[str]): Query. Defaults to None.

        """
        response_text = response.response
        source_nodes = [n.dict() for n in response.source_nodes]
        json_dict = {
            "response": response_text,
            "source_nodes": source_nodes,
            "query": query,
        }
        r = requests.post(webhook_url, json=json_dict)
        r.raise_for_status()
