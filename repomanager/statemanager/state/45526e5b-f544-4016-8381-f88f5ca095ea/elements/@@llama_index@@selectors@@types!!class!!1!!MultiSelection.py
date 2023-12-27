class MultiSelection(BaseModel):
    """A multi-selection of choices."""

    selections: List[SingleSelection]

    @property
    def ind(self) -> int:
        if len(self.selections) != 1:
            raise ValueError(
                f"There are {len(self.selections)} selections, " "please use .inds."
            )
        return self.selections[0].index

    @property
    def reason(self) -> str:
        if len(self.reasons) != 1:
            raise ValueError(
                f"There are {len(self.reasons)} selections, " "please use .reasons."
            )
        return self.selections[0].reason

    @property
    def inds(self) -> List[int]:
        return [x.index for x in self.selections]

    @property
    def reasons(self) -> List[str]:
        return [x.reason for x in self.selections]
