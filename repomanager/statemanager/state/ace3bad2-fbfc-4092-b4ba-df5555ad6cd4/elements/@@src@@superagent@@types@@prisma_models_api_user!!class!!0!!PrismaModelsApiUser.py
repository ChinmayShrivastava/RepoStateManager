class PrismaModelsApiUser(pydantic.BaseModel):
    """
    Represents a ApiUser record
    """

    id: str
    token: typing.Optional[str]
    email: typing.Optional[str]
    created_at: dt.datetime = pydantic.Field(alias="createdAt")
    updated_at: dt.datetime = pydantic.Field(alias="updatedAt")
    agents: typing.Optional[typing.List[PrismaModelsAgent]]
    llms: typing.Optional[typing.List[PrismaModelsLlm]]
    datasources: typing.Optional[typing.List[PrismaModelsDatasource]]
    tools: typing.Optional[typing.List[PrismaModelsTool]]
    workflows: typing.Optional[typing.List[PrismaModelsWorkflow]]

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