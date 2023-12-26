class LlmModel(str, enum.Enum):
    """
    An enumeration.
    """

    GPT_3_5_TURBO_16_K_0613 = "GPT_3_5_TURBO_16K_0613"
    GPT_3_5_TURBO_0613 = "GPT_3_5_TURBO_0613"
    GPT_3_5_TURBO_1106 = "GPT_3_5_TURBO_1106"
    GPT_4_0613 = "GPT_4_0613"
    GPT_4_32_K_0613 = "GPT_4_32K_0613"
    GPT_4_1106_PREVIEW = "GPT_4_1106_PREVIEW"
    MISTRAL_7_B_INSTRUCT_V_01 = "MISTRAL_7B_INSTRUCT_V01"

    def visit(
        self,
        gpt_3_5_turbo_16_k_0613: typing.Callable[[], T_Result],
        gpt_3_5_turbo_0613: typing.Callable[[], T_Result],
        gpt_3_5_turbo_1106: typing.Callable[[], T_Result],
        gpt_4_0613: typing.Callable[[], T_Result],
        gpt_4_32_k_0613: typing.Callable[[], T_Result],
        gpt_4_1106_preview: typing.Callable[[], T_Result],
        mistral_7_b_instruct_v_01: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is LlmModel.GPT_3_5_TURBO_16_K_0613:
            return gpt_3_5_turbo_16_k_0613()
        if self is LlmModel.GPT_3_5_TURBO_0613:
            return gpt_3_5_turbo_0613()
        if self is LlmModel.GPT_3_5_TURBO_1106:
            return gpt_3_5_turbo_1106()
        if self is LlmModel.GPT_4_0613:
            return gpt_4_0613()
        if self is LlmModel.GPT_4_32_K_0613:
            return gpt_4_32_k_0613()
        if self is LlmModel.GPT_4_1106_PREVIEW:
            return gpt_4_1106_preview()
        if self is LlmModel.MISTRAL_7_B_INSTRUCT_V_01:
            return mistral_7_b_instruct_v_01()
