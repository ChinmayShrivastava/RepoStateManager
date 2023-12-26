class DatasourceStatus(str, enum.Enum):
    """
    An enumeration.
    """

    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"

    def visit(
        self,
        in_progress: typing.Callable[[], T_Result],
        done: typing.Callable[[], T_Result],
        failed: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is DatasourceStatus.IN_PROGRESS:
            return in_progress()
        if self is DatasourceStatus.DONE:
            return done()
        if self is DatasourceStatus.FAILED:
            return failed()
