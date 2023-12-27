class ServiceContextData(BaseModel):
    llm: dict
    llm_predictor: dict
    prompt_helper: dict
    embed_model: dict
    transformations: List[dict]
