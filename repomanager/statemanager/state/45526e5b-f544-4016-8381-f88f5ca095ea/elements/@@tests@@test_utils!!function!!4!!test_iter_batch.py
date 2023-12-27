def test_iter_batch() -> None:
    """Check iter_batch works as expected on regular, lazy and empty sequences."""
    lst = list(range(6))
    assert list(iter_batch(lst, 3)) == [[0, 1, 2], [3, 4, 5]]

    gen = (i for i in range(5))
    assert list(iter_batch(gen, 3)) == [[0, 1, 2], [3, 4]]

    assert list(iter_batch([], 3)) == []
