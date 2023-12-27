class BufferedAsyncIterator(ABC):
    """
    Base class for buffered async iterators.

    This class is to be used as a base class for async iterators
    that need to buffer the results of an async operation.
    The async operation is defined in the _fill_buffer method.
    The _fill_buffer method is called when the buffer is empty.
    """

    def __init__(self, buffer_size: int):
        """
        Initialize params.

        Args:
            - `buffer_size (int)`: Size of the buffer.
                It is also the number of items that will
                be retrieved from the async operation at once.
                see _fill_buffer. Defaults to 2. Setting it to 1
                will result in the same behavior as a synchronous iterator.
        """
        self._buffer_size = buffer_size
        self._buffer: List[Tuple[GitBlobResponseModel, str]] = []
        self._index = 0

    @abstractmethod
    async def _fill_buffer(self) -> None:
        raise NotImplementedError

    def __aiter__(self) -> "BufferedAsyncIterator":
        """Return the iterator object."""
        return self

    async def __anext__(self) -> Tuple[GitBlobResponseModel, str]:
        """
        Get next item.

        Returns:
            - `item (Tuple[GitBlobResponseModel, str])`: Next item.

        Raises:
            - `StopAsyncIteration`: If there are no more items.
        """
        if not self._buffer:
            await self._fill_buffer()

        if not self._buffer:
            raise StopAsyncIteration

        item = self._buffer.pop(0)
        self._index += 1
        return item
