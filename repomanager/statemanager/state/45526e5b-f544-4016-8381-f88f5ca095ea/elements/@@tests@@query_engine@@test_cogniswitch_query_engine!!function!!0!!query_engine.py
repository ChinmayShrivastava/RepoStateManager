def query_engine() -> CogniswitchQueryEngine:
    return CogniswitchQueryEngine(
        cs_token="cs_token", OAI_token="OAI_token", apiKey="api_key"
    )
