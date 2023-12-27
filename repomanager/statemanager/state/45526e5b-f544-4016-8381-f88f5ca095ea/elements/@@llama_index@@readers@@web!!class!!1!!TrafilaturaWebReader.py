class TrafilaturaWebReader(BasePydanticReader):
    """Trafilatura web page reader.

    Reads pages from the web.
    Requires the `trafilatura` package.

    """

    is_remote: bool = True
    error_on_missing: bool

    def __init__(self, error_on_missing: bool = False) -> None:
        """Initialize with parameters.

        Args:
            error_on_missing (bool): Throw an error when data cannot be parsed
        """
        try:
            import trafilatura  # noqa
        except ImportError:
            raise ImportError(
                "`trafilatura` package not found, please run `pip install trafilatura`"
            )
        super().__init__(error_on_missing=error_on_missing)

    @classmethod
    def class_name(cls) -> str:
        return "TrafilaturaWebReader"

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        import trafilatura

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []
        for url in urls:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                if self.error_on_missing:
                    raise ValueError(f"Trafilatura fails to get string from url: {url}")
                continue
            response = trafilatura.extract(downloaded)
            if not response:
                if self.error_on_missing:
                    raise ValueError(f"Trafilatura fails to parse page: {url}")
                continue
            documents.append(Document(text=response))

        return documents
