class MockObject1(PromptMixin):
    def __init__(self) -> None:
        self.mock_object_2 = MockObject2()
        self._prompt_dict_1 = {
            "summary": PromptTemplate("{summary}"),
            "foo": PromptTemplate("{foo} {bar}"),
        }

    def _get_prompts(self) -> PromptDictType:
        return self._prompt_dict_1

    def _get_prompt_modules(self) -> PromptMixinType:
        return {"mock_object_2": self.mock_object_2}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        if "summary" in prompts:
            self._prompt_dict_1["summary"] = prompts["summary"]
        if "foo" in prompts:
            self._prompt_dict_1["foo"] = prompts["foo"]
