def mock_chat(*args: Any, **kwargs: Any) -> Union[Any, "AI21Object"]:
    return construct_ai21_object(
        {
            "id": "f8d0cd0a-7c85-deb2-16b3-491c7ffdd4f2",
            "prompt": {
                "text": "user: This is just a test assistant:",
                "tokens": [
                    {
                        "generatedToken": {
                            "token": "▁user",
                            "logprob": -13.633946418762207,
                            "raw_logprob": -13.633946418762207,
                        },
                        "topTokens": None,
                        "textRange": {"start": 0, "end": 4},
                    },
                    {
                        "generatedToken": {
                            "token": ":",
                            "logprob": -5.545032978057861,
                            "raw_logprob": -5.545032978057861,
                        },
                        "topTokens": None,
                        "textRange": {"start": 4, "end": 5},
                    },
                    {
                        "generatedToken": {
                            "token": "▁This▁is▁just",
                            "logprob": -10.848762512207031,
                            "raw_logprob": -10.848762512207031,
                        },
                        "topTokens": None,
                        "textRange": {"start": 5, "end": 18},
                    },
                    {
                        "generatedToken": {
                            "token": "▁a▁test",
                            "logprob": -2.0551252365112305,
                            "raw_logprob": -2.0551252365112305,
                        },
                        "topTokens": None,
                        "textRange": {"start": 18, "end": 25},
                    },
                    {
                        "generatedToken": {
                            "token": "▁assistant",
                            "logprob": -17.020610809326172,
                            "raw_logprob": -17.020610809326172,
                        },
                        "topTokens": None,
                        "textRange": {"start": 25, "end": 35},
                    },
                    {
                        "generatedToken": {
                            "token": ":",
                            "logprob": -12.311965942382812,
                            "raw_logprob": -12.311965942382812,
                        },
                        "topTokens": None,
                        "textRange": {"start": 35, "end": 36},
                    },
                ],
            },
            "completions": [
                {
                    "data": {
                        "text": "\nassistant:\nHow can I assist you today?",
                        "tokens": [
                            {
                                "generatedToken": {
                                    "token": "<|newline|>",
                                    "logprob": 0,
                                    "raw_logprob": -0.02031332440674305,
                                },
                                "topTokens": None,
                                "textRange": {"start": 0, "end": 1},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁assistant",
                                    "logprob": 0,
                                    "raw_logprob": -0.24520651996135712,
                                },
                                "topTokens": None,
                                "textRange": {"start": 1, "end": 10},
                            },
                            {
                                "generatedToken": {
                                    "token": ":",
                                    "logprob": 0,
                                    "raw_logprob": -0.0026112052146345377,
                                },
                                "topTokens": None,
                                "textRange": {"start": 10, "end": 11},
                            },
                            {
                                "generatedToken": {
                                    "token": "<|newline|>",
                                    "logprob": 0,
                                    "raw_logprob": -0.3382393717765808,
                                },
                                "topTokens": None,
                                "textRange": {"start": 11, "end": 12},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁How▁can▁I",
                                    "logprob": -0.000008106198947643861,
                                    "raw_logprob": -1.3073582649230957,
                                },
                                "topTokens": None,
                                "textRange": {"start": 12, "end": 21},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁assist▁you",
                                    "logprob": -2.15450382232666,
                                    "raw_logprob": -0.8163930177688599,
                                },
                                "topTokens": None,
                                "textRange": {"start": 21, "end": 32},
                            },
                            {
                                "generatedToken": {
                                    "token": "▁today",
                                    "logprob": 0,
                                    "raw_logprob": -0.1474292278289795,
                                },
                                "topTokens": None,
                                "textRange": {"start": 32, "end": 38},
                            },
                            {
                                "generatedToken": {
                                    "token": "?",
                                    "logprob": 0,
                                    "raw_logprob": -0.011986607685685158,
                                },
                                "topTokens": None,
                                "textRange": {"start": 38, "end": 39},
                            },
                            {
                                "generatedToken": {
                                    "token": "<|endoftext|>",
                                    "logprob": -1.1920928244535389e-7,
                                    "raw_logprob": -0.2295214682817459,
                                },
                                "topTokens": None,
                                "textRange": {"start": 39, "end": 39},
                            },
                        ],
                    },
                    "finishReason": {"reason": "endoftext"},
                }
            ],
        }
    )
