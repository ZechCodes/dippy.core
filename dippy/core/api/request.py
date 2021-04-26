from bevy import Injectable
from dippy.core.api.bases import BaseDiscordAPI
from typing import Any, Optional
from urllib.parse import urlencode, SplitResult
from json import dumps


class Request(Injectable):
    __api_version__ = 8

    api: BaseDiscordAPI

    def __init__(self, endpoint: str):
        self._endpoint = endpoint.strip("/")

    async def delete(self, **kwargs):
        return await self.api.session.delete(self._create_url(kwargs))

    async def get(self, **kwargs):
        return await self.api.session.get(self._create_url(kwargs))

    async def post(self, **kwargs):
        content_type = "application/json"
        print(kwargs)
        return await self.api.session.post(
            self._create_url(),
            data=self._to_json(kwargs),
            headers={"Content-Type": content_type},
        )

    def _create_url(self, query_args: Optional[dict[str, Any]] = None) -> str:
        url = SplitResult(
            scheme="https",
            netloc="discord.com",
            path=f"/api/v{self.__api_version__}/{self._endpoint}",
            query=urlencode(query_args) if query_args else "",
            fragment="",
        )
        return url.geturl()

    def _to_json(self, content: dict[str, Any]) -> str:
        return dumps(content, separators=(",", ":"), ensure_ascii=True)
