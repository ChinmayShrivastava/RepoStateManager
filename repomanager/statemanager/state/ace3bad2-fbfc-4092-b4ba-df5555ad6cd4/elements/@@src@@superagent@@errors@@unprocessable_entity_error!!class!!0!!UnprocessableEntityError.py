class UnprocessableEntityError(ApiError):
    def __init__(self, body: HttpValidationError):
        super().__init__(status_code=422, body=body)
