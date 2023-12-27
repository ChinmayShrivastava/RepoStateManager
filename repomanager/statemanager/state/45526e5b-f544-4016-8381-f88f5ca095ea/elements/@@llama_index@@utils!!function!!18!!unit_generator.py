def unit_generator(x: Any) -> Generator[Any, None, None]:
    """A function that returns a generator of a single element.

    Args:
        x (Any): the element to build yield

    Yields:
        Any: the single element
    """
    yield x
