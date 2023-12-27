class DiscordReader(BasePydanticReader):
    """Discord reader.

    Reads conversations from channels.

    Args:
        discord_token (Optional[str]): Discord token. If not provided, we
            assume the environment variable `DISCORD_TOKEN` is set.

    """

    is_remote: bool = True
    discord_token: str

    def __init__(self, discord_token: Optional[str] = None) -> None:
        """Initialize with parameters."""
        try:
            import discord  # noqa
        except ImportError:
            raise ImportError(
                "`discord.py` package not found, please run `pip install discord.py`"
            )
        if discord_token is None:
            discord_token = os.environ["DISCORD_TOKEN"]
            if discord_token is None:
                raise ValueError(
                    "Must specify `discord_token` or set environment "
                    "variable `DISCORD_TOKEN`."
                )

        super().__init__(discord_token=discord_token)

    @classmethod
    def class_name(cls) -> str:
        return "DiscordReader"

    def _read_channel(
        self, channel_id: int, limit: Optional[int] = None, oldest_first: bool = True
    ) -> List[Document]:
        """Read channel."""
        return asyncio.get_event_loop().run_until_complete(
            read_channel(
                self.discord_token, channel_id, limit=limit, oldest_first=oldest_first
            )
        )

    def load_data(
        self,
        channel_ids: List[int],
        limit: Optional[int] = None,
        oldest_first: bool = True,
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            channel_ids (List[int]): List of channel ids to read.
            limit (Optional[int]): Maximum number of messages to read.
            oldest_first (bool): Whether to read oldest messages first.
                Defaults to `True`.

        Returns:
            List[Document]: List of documents.

        """
        results: List[Document] = []
        for channel_id in channel_ids:
            if not isinstance(channel_id, int):
                raise ValueError(
                    f"Channel id {channel_id} must be an integer, "
                    f"not {type(channel_id)}."
                )
            channel_documents = self._read_channel(
                channel_id, limit=limit, oldest_first=oldest_first
            )
            results += channel_documents
        return results
