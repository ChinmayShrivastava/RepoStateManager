class PrismaModelsWorkflow(pydantic.BaseModel):
    """
    Represents a Workflow record
    """

    id: str
    name: str
    description: typing.Optional[str]
    created_at: dt.datetime = pydantic.Field(alias="createdAt")
    updated_at: dt.datetime = pydantic.Field(alias="updatedAt")
    steps: typing.Optional[typing.List[PrismaModelsWorkflowStep]]
    api_user_id: str = pydantic.Field(alias="apiUserId")
    api_user: typing.Optional[PrismaModelsApiUser] = pydantic.Field(alias="apiUser")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
