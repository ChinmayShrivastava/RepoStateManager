    class CustomTransport(AsyncTransport):
        requests = []

        async def perform_request(self, *args, **kwargs):  # type: ignore
            self.requests.append(kwargs)
            return await super().perform_request(*args, **kwargs)
