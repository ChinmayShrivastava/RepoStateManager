class MockObject2(PromptMixin):
    def __init__(self) -> None:
        self._prompt_dict_2 = {
            "abc": PromptTemplate("{abc} {def}"),
        }

    def _get_prompts(self) -> PromptDictType:
        return self._prompt_dict_2

    def _get_prompt_modules(self) -> PromptMixinType:
        return {}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        if "abc" in prompts:
            self._prompt_dict_2["abc"] = prompts["abc"]
