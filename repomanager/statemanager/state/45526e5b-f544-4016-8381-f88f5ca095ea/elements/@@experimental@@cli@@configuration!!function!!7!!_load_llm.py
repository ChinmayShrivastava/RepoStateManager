def _load_llm(section: SectionProxy) -> LLM:
    if "engine" in section:
        return OpenAI(engine=section["engine"])
    else:
        return OpenAI()
