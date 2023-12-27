        def wrapper(*args: Any, **kwargs: Any) -> None:
            """Callcuate time taken to run a function."""
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(f"Time taken: {end - start} seconds for {func.__name__}")
