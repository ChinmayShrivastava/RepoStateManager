class IdFuncCallable(Protocol):
    def __call__(self, i: int, doc: BaseNode) -> str:
        ...