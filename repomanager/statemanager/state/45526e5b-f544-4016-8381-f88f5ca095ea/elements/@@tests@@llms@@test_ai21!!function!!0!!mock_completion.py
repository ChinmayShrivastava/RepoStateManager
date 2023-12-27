def mock_completion(*args: Any, **kwargs: Any) -> Union[Any, "AI21Object"]:
    return construct_ai21_object(
        {
            "id": "f6adacef-0e94-6353-244f-df8d38954b19",
            "prompt": {
                "text": "This is just a test",
                "tokens": [
                    {
                        "generatedToken": {
                            "token": "▁This▁is▁just",
                            "logprob": -13.657383918762207,
                            "raw_logprob": -13.657383918762207,
                        },
                        "topTokens": None,
                        "textRange": {"start": 0, "end": 12},
                    },
                    {
                        "generatedToken": {
                            "token": "▁a▁test",
                            "logprob": -4.080351829528809,
                            "raw_logprob": -4.080351829528809,
                        },
                        "topTokens": None,
                        "textRange": {"start": 12, "end": 19},
                    },
                ],
            },
            "completions": [
                {
                    "data": {
                        "text": "\nThis is a test to see if my text is showing up correctly.",
                        "tokens": [
                            {
                                "generatedToken": {
                                    "token": "<|newline|>",
                                    "logprob": 0,
                                    "raw_logprob": -0.01992332935333252,
                                },
                                "topTokens": None,
                                "textRange": {"start": 0, "end": 1},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁This▁is▁a",
                                    "logprob": -0.00014733182615600526,
                                    "raw_logprob": -1.228371500968933,
                                },
                                "topTokens": None,
                                "textRange": {"start": 1, "end": 10},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁test",
                                    "logprob": 0,
                                    "raw_logprob": -0.0422857291996479,
                                },
                                "topTokens": None,
                                "textRange": {"start": 10, "end": 15},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁to▁see▁if",
                                    "logprob": -0.4861462712287903,
                                    "raw_logprob": -1.2263909578323364,
                                },
                                "topTokens": None,
                                "textRange": {"start": 15, "end": 25},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁my",
                                    "logprob": -9.536738616588991e-7,
                                    "raw_logprob": -0.8164164423942566,
                                },
                                "topTokens": None,
                                "textRange": {"start": 25, "end": 28},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁text",
                                    "logprob": -0.003087161108851433,
                                    "raw_logprob": -1.7130306959152222,
                                },
                                "topTokens": None,
                                "textRange": {"start": 28, "end": 33},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁is",
                                    "logprob": -1.8836627006530762,
                                    "raw_logprob": -0.9880049824714661,
                                },
                                "topTokens": None,
                                "textRange": {"start": 33, "end": 36},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁showing▁up",
                                    "logprob": -0.00006341733387671411,
                                    "raw_logprob": -0.954255223274231,
                                },
                                "topTokens": None,
                                "textRange": {"start": 36, "end": 47},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁correctly",
                                    "logprob": -0.00022098960471339524,
                                    "raw_logprob": -0.6004139184951782,
                                },
                                "topTokens": None,
                                "textRange": {"start": 47, "end": 57},
                            },
                            {
                                "generatedToken": {
                                    "token": ".",
                                    "logprob": 0,
                                    "raw_logprob": -0.039214372634887695,
                                },
                                "topTokens": None,
                                "textRange": {"start": 57, "end": 58},
                            },
                            {
                                "generatedToken": {
                                    "token": "<|endoftext|>",
                                    "logprob": 0,
                                    "raw_logprob": -0.22456447780132294,
                                },
                                "topTokens": None,
                                "textRange": {"start": 58, "end": 58},
                            },
                        ],
                    },
                    "finishReason": {"reason": "endoftext"},
                }
            ],
        }
    )
