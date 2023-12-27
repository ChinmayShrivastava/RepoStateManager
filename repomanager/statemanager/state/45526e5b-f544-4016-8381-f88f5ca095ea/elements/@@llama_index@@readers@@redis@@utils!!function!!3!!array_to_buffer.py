def array_to_buffer(array: List[float], dtype: Any = np.float32) -> bytes:
    return np.array(array).astype(dtype).tobytes()
