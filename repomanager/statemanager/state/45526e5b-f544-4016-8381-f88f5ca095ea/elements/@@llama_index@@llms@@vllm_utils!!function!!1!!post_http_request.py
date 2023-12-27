def post_http_request(
    api_url: str, sampling_params: dict = {}, stream: bool = False
) -> requests.Response:
    headers = {"User-Agent": "Test Client"}
    sampling_params["stream"] = stream

    return requests.post(api_url, headers=headers, json=sampling_params, stream=True)
