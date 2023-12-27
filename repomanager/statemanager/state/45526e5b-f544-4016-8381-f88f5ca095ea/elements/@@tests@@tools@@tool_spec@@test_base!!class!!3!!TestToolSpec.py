class TestToolSpec(BaseToolSpec):
    spec_functions: List[Union[str, Tuple[str, str]]] = ["foo", "bar", "abc"]

    def foo(self, arg1: str, arg2: int) -> str:
        """Foo."""
        return f"foo {arg1} {arg2}"

    def bar(self, arg1: bool) -> str:
        """Bar."""
        return f"bar {arg1}"

    async def afoo(self, arg1: str, arg2: int) -> str:
        """Afoo."""
        return self.foo(arg1=arg1, arg2=arg2)

    async def abar(self, arg1: bool) -> str:
        """Abar."""
        return self.bar(arg1=arg1)

    def abc(self, arg1: str) -> str:
        # NOTE: no docstring
        return f"bar {arg1}"

    def get_fn_schema_from_fn_name(self, fn_name: str) -> Type[BaseModel]:
        """Return map from function name."""
        if fn_name == "foo":
            return FooSchema
        elif fn_name == "afoo":
            return FooSchema
        elif fn_name == "bar":
            return BarSchema
        elif fn_name == "abc":
            return AbcSchema
        else:
            raise ValueError(f"Invalid function name: {fn_name}")
