class BeautifulSoupWebReader(BasePydanticReader):
    """BeautifulSoup web page reader.

    Reads pages from the web.
    Requires the `bs4` and `urllib` packages.

    Args:
        website_extractor (Optional[Dict[str, Callable]]): A mapping of website
            hostname (e.g. google.com) to a function that specifies how to
            extract text from the BeautifulSoup obj. See DEFAULT_WEBSITE_EXTRACTOR.
    """

    is_remote: bool = True
    _website_extractor: Dict[str, Callable] = PrivateAttr()

    def __init__(
        self,
        website_extractor: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """Initialize with parameters."""
        try:
            from urllib.parse import urlparse  # noqa

            import requests  # noqa
            from bs4 import BeautifulSoup  # noqa
        except ImportError:
            raise ImportError(
                "`bs4`, `requests`, and `urllib` must be installed to scrape websites."
                "Please run `pip install bs4 requests urllib`."
            )

        self._website_extractor = website_extractor or DEFAULT_WEBSITE_EXTRACTOR
        super().__init__()

    @classmethod
    def class_name(cls) -> str:
        return "BeautifulSoupWebReader"

    def load_data(
        self, urls: List[str], custom_hostname: Optional[str] = None
    ) -> List[Document]:
        """Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.
            custom_hostname (Optional[str]): Force a certain hostname in the case
                a website is displayed under custom URLs (e.g. Substack blogs)

        Returns:
            List[Document]: List of documents.

        """
        from urllib.parse import urlparse

        import requests
        from bs4 import BeautifulSoup

        documents = []
        for url in urls:
            try:
                page = requests.get(url)
            except Exception:
                raise ValueError(f"One of the inputs is not a valid url: {url}")

            hostname = custom_hostname or urlparse(url).hostname or ""

            soup = BeautifulSoup(page.content, "html.parser")

            data = ""
            metadata = {"URL": url}
            if hostname in self._website_extractor:
                data, metadata = self._website_extractor[hostname](soup)
                metadata.update(metadata)
            else:
                data = soup.getText()

            documents.append(Document(text=data, metadata=metadata))

        return documents
