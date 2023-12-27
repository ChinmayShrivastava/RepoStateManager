class BufferedGitBlobDataIterator(BufferedAsyncIterator):
    """
    Buffered async iterator for Git blobs.

    This class is an async iterator that buffers the results of the get_blob operation.
    It is used to retrieve the contents of the files in a Github repository.
    getBlob endpoint supports up to 100 megabytes of content for blobs.
    This concrete implementation of BufferedAsyncIterator allows you to lazily retrieve
    the contents of the files in a Github repository.
    Otherwise you would have to retrieve all the contents of
    the files in the repository at once, which would
    be problematic if the repository is large.
    """

    def __init__(
        self,
        blobs_and_paths: List[Tuple[GitTreeResponseModel.GitTreeObject, str]],
        github_client: GithubClient,
        owner: str,
        repo: str,
        loop: asyncio.AbstractEventLoop,
        buffer_size: int,
        verbose: bool = False,
    ):
        """
        Initialize params.

        Args:
            - blobs_and_paths (List[Tuple[GitTreeResponseModel.GitTreeObject, str]]):
                List of tuples containing the blob and the path of the file.
            - github_client (GithubClient): Github client.
            - owner (str): Owner of the repository.
            - repo (str): Name of the repository.
            - loop (asyncio.AbstractEventLoop): Event loop.
            - buffer_size (int): Size of the buffer.
        """
        super().__init__(buffer_size)
        self._blobs_and_paths = blobs_and_paths
        self._github_client = github_client
        self._owner = owner
        self._repo = repo
        self._verbose = verbose
        if loop is None:
            loop = asyncio.get_event_loop()
            if loop is None:
                raise ValueError("No event loop found")

    async def _fill_buffer(self) -> None:
        """
        Fill the buffer with the results of the get_blob operation.

        The get_blob operation is called for each blob in the blobs_and_paths list.
        The blobs are retrieved in batches of size buffer_size.
        """
        del self._buffer[:]
        self._buffer = []
        start = self._index
        end = min(start + self._buffer_size, len(self._blobs_and_paths))

        if start >= end:
            return

        if self._verbose:
            start_t = time.time()
        results: List[GitBlobResponseModel] = await asyncio.gather(
            *[
                self._github_client.get_blob(self._owner, self._repo, blob.sha)
                for blob, _ in self._blobs_and_paths[
                    start:end
                ]  # TODO: use batch_size instead of buffer_size for concurrent requests
            ]
        )
        if self._verbose:
            end_t = time.time()
            blob_names_and_sizes = [
                (blob.path, blob.size) for blob, _ in self._blobs_and_paths[start:end]
            ]
            print(
                "Time to get blobs ("
                + f"{blob_names_and_sizes}"
                + f"): {end_t - start_t:.2f} seconds"
            )

        self._buffer = [
            (result, path)
            for result, (_, path) in zip(results, self._blobs_and_paths[start:end])
        ]
