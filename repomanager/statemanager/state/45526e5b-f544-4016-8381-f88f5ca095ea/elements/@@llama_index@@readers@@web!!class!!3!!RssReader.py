class RssReader(BasePydanticReader):
    """RSS reader.

    Reads content from an RSS feed.

    """

    is_remote: bool = True
    html_to_text: bool

    def __init__(self, html_to_text: bool = False) -> None:
        """Initialize with parameters.

        Args:
            html_to_text (bool): Whether to convert HTML to text.
                Requires `html2text` package.

        """
        try:
            import feedparser  # noqa
        except ImportError:
            raise ImportError(
                "`feedparser` package not found, please run `pip install feedparser`"
            )

        if html_to_text:
            try:
                import html2text  # noqa
            except ImportError:
                raise ImportError(
                    "`html2text` package not found, please run `pip install html2text`"
                )
        super().__init__(html_to_text=html_to_text)

    @classmethod
    def class_name(cls) -> str:
        return "RssReader"

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from RSS feeds.

        Args:
            urls (List[str]): List of RSS URLs to load.

        Returns:
            List[Document]: List of documents.

        """
        import feedparser

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")

        documents = []

        for url in urls:
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                if "content" in entry:
                    data = entry.content[0].value
                else:
                    data = entry.description or entry.summary

                if self.html_to_text:
                    import html2text

                    data = html2text.html2text(data)

                metadata = {"title": entry.title, "link": entry.link}
                documents.append(Document(text=data, metadata=metadata))

        return documents
