class PrismaModelsAgent(pydantic.BaseModel):
    """
    Represents a Agent record
    """

    id: str
    name: str
    avatar: typing.Optional[str]
    initial_message: typing.Optional[str] = pydantic.Field(alias="initialMessage")
    description: str
    is_active: bool = pydantic.Field(alias="isActive")
    created_at: dt.datetime = pydantic.Field(alias="createdAt")
    updated_at: dt.datetime = pydantic.Field(alias="updatedAt")
    llms: typing.Optional[typing.List[PrismaModelsAgentLlm]]
    llm_model: LlmModel = pydantic.Field(alias="llmModel")
    prompt: typing.Optional[str]
    api_user_id: str = pydantic.Field(alias="apiUserId")
    api_user: typing.Optional[PrismaModelsApiUser] = pydantic.Field(alias="apiUser")
    datasources: typing.Optional[typing.List[PrismaModelsAgentDatasource]]
    tools: typing.Optional[typing.List[PrismaModelsAgentTool]]
    workflow_steps: typing.Optional[typing.List[PrismaModelsWorkflowStep]] = pydantic.Field(alias="workflowSteps")

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
