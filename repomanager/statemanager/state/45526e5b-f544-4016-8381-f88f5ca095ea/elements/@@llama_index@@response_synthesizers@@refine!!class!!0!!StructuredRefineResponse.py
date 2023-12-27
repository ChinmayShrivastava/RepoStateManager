class StructuredRefineResponse(BaseModel):
    """
    Used to answer a given query based on the provided context.

    Also indicates if the query was satisfied with the provided answer.
    """

    answer: str = Field(
        description="The answer for the given query, based on the context and not "
        "prior knowledge."
    )
    query_satisfied: bool = Field(
        description="True if there was enough context given to provide an answer "
        "that satisfies the query."
    )
