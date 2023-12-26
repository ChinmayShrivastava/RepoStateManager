class PrismaModelsAgentLlm(pydantic.BaseModel):
    """
    Represents a AgentLLM record
    """

    agent_id: str = pydantic.Field(alias="agentId")
    llm_id: str = pydantic.Field(alias="llmId")
    agent: typing.Optional[PrismaModelsAgent]
    llm: typing.Optional[PrismaModelsLlm]
    created_at: dt.datetime = pydantic.Field(alias="createdAt")
    updated_at: dt.datetime = pydantic.Field(alias="updatedAt")

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
