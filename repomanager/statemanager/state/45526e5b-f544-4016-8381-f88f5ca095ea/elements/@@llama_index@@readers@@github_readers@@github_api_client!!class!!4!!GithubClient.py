class GithubClient:
    """
    An asynchronous client for interacting with the Github API.

    This client is used for making API requests to Github.
    It provides methods for accessing the Github API endpoints.
    The client requires a Github token for authentication,
    which can be passed as an argument or set as an environment variable.
    If no Github token is provided, the client will raise a ValueError.

    Examples:
        >>> client = GithubClient("my_github_token")
        >>> branch_info = client.get_branch("owner", "repo", "branch")
    """

    DEFAULT_BASE_URL = "https://api.github.com"
    DEFAULT_API_VERSION = "2022-11-28"

    def __init__(
        self,
        github_token: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        verbose: bool = False,
    ) -> None:
        """
        Initialize the GithubClient.

        Args:
            - github_token (str): Github token for authentication.
                If not provided, the client will try to get it from
                the GITHUB_TOKEN environment variable.
            - base_url (str): Base URL for the Github API
                (defaults to "https://api.github.com").
            - api_version (str): Github API version (defaults to "2022-11-28").

        Raises:
            ValueError: If no Github token is provided.
        """
        if github_token is None:
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token is None:
                raise ValueError(
                    "Please provide a Github token. "
                    + "You can do so by passing it as an argument to the GithubReader,"
                    + "or by setting the GITHUB_TOKEN environment variable."
                )

        self._base_url = base_url
        self._api_version = api_version
        self._verbose = verbose

        self._endpoints = {
            "getTree": "/repos/{owner}/{repo}/git/trees/{tree_sha}",
            "getBranch": "/repos/{owner}/{repo}/branches/{branch}",
            "getBlob": "/repos/{owner}/{repo}/git/blobs/{file_sha}",
            "getCommit": "/repos/{owner}/{repo}/commits/{commit_sha}",
        }

        self._headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": f"{self._api_version}",
        }

    def get_all_endpoints(self) -> Dict[str, str]:
        """Get all available endpoints."""
        return {**self._endpoints}

    async def request(
        self,
        endpoint: str,
        method: str,
        headers: Dict[str, Any] = {},
        **kwargs: Any,
    ) -> Any:
        """
        Make an API request to the Github API.

        This method is used for making API requests to the Github API.
        It is used internally by the other methods in the client.

        Args:
            - `endpoint (str)`: Name of the endpoint to make the request to.
            - `method (str)`: HTTP method to use for the request.
            - `headers (dict)`: HTTP headers to include in the request.
            - `**kwargs`: Keyword arguments to pass to the endpoint URL.

        Returns:
            - `response (httpx.Response)`: Response from the API request.

        Raises:
            - ImportError: If the `httpx` library is not installed.
            - httpx.HTTPError: If the API request fails.

        Examples:
            >>> response = client.request("getTree", "GET",
                                owner="owner", repo="repo",
                                tree_sha="tree_sha")
        """
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "Please install httpx to use the GithubRepositoryReader. "
                "You can do so by running `pip install httpx`."
            )

        _headers = {**self._headers, **headers}

        _client: httpx.AsyncClient
        async with httpx.AsyncClient(
            headers=_headers, base_url=self._base_url
        ) as _client:
            try:
                response = await _client.request(
                    method, url=self._endpoints[endpoint].format(**kwargs)
                )
                response.raise_for_status()
            except httpx.HTTPError as excp:
                print(f"HTTP Exception for {excp.request.url} - {excp}")
                raise
            return response

    async def get_branch(
        self, owner: str, repo: str, branch: str
    ) -> GitBranchResponseModel:
        """
        Get information about a branch. (Github API endpoint: getBranch).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `branch (str)`: Name of the branch.

        Returns:
            - `branch_info (GitBranchResponseModel)`: Information about the branch.

        Examples:
            >>> branch_info = client.get_branch("owner", "repo", "branch")
        """
        return GitBranchResponseModel.from_json(
            (
                await self.request(
                    "getBranch", "GET", owner=owner, repo=repo, branch=branch
                )
            ).text
        )

    async def get_tree(
        self, owner: str, repo: str, tree_sha: str
    ) -> GitTreeResponseModel:
        """
        Get information about a tree. (Github API endpoint: getTree).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `tree_sha (str)`: SHA of the tree.

        Returns:
            - `tree_info (GitTreeResponseModel)`: Information about the tree.

        Examples:
            >>> tree_info = client.get_tree("owner", "repo", "tree_sha")
        """
        return GitTreeResponseModel.from_json(
            (
                await self.request(
                    "getTree", "GET", owner=owner, repo=repo, tree_sha=tree_sha
                )
            ).text
        )

    async def get_blob(
        self, owner: str, repo: str, file_sha: str
    ) -> GitBlobResponseModel:
        """
        Get information about a blob. (Github API endpoint: getBlob).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `file_sha (str)`: SHA of the file.

        Returns:
            - `blob_info (GitBlobResponseModel)`: Information about the blob.

        Examples:
            >>> blob_info = client.get_blob("owner", "repo", "file_sha")
        """
        return GitBlobResponseModel.from_json(
            (
                await self.request(
                    "getBlob", "GET", owner=owner, repo=repo, file_sha=file_sha
                )
            ).text
        )

    async def get_commit(
        self, owner: str, repo: str, commit_sha: str
    ) -> GitCommitResponseModel:
        """
        Get information about a commit. (Github API endpoint: getCommit).

        Args:
            - `owner (str)`: Owner of the repository.
            - `repo (str)`: Name of the repository.
            - `commit_sha (str)`: SHA of the commit.

        Returns:
            - `commit_info (GitCommitResponseModel)`: Information about the commit.

        Examples:
            >>> commit_info = client.get_commit("owner", "repo", "commit_sha")
        """
        return GitCommitResponseModel.from_json(
            (
                await self.request(
                    "getCommit", "GET", owner=owner, repo=repo, commit_sha=commit_sha
                )
            ).text
        )
