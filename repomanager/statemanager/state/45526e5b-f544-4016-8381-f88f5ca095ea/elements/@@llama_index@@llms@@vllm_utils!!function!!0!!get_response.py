def get_response(response: requests.Response) -> List[str]:
    data = json.loads(response.content)
    return data["text"]
