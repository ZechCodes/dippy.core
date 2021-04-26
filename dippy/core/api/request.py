from aiohttp import FormData
from bevy import Injectable
from dippy.core.api.bases import BaseDiscordAPI
from io import IOBase
from typing import Any, Optional
from urllib.parse import quote, SplitResult, urlencode
from json import dumps
from mimetypes import guess_type


class Request(Injectable):
    __api_version__ = 8

    api: BaseDiscordAPI

    def __init__(self, endpoint: str):
        self._endpoint = endpoint.strip("/")

    async def delete(self, **kwargs):
        resp = await self.api.session.delete(self._create_url(kwargs))
        return await self._get_response(resp), resp.status

    async def get(self, **kwargs):
        resp = await self.api.session.get(self._create_url(kwargs))
        return await self._get_response(resp), resp.status

    async def post(
        self,
        files: Optional[dict[str, IOBase]] = None,
        reason: Optional[str] = None,
        **kwargs,
    ):
        data = self._to_json(kwargs)
        headers = {}
        if files:
            json_data, data = data, FormData()
            data.add_field(name="payload_json", value=json_data)

            namer = "file{}".format if len(files) > 1 else lambda _: "file"
            for index, (filename, file) in enumerate(files.items()):
                data.add_field(
                    name=namer(index),
                    value=file,
                    filename=filename,
                    content_type=guess_type(filename)[0] or "application/octet-stream",
                )
        else:
            headers["Content-Type"] = "application/json"

        if reason:
            headers["X-Audit-Log-Reason"] = quote(reason, safe="/ ")

        response = await self.api.session.post(
            self._create_url(), data=data, headers=headers
        )
        return await self._get_response(response), response.status

    async def put(self, **kwargs):
        resp = await self.api.session.put(self._create_url(kwargs))
        return await self._get_response(resp), resp.status

    def _create_url(self, query_args: Optional[dict[str, Any]] = None) -> str:
        url = SplitResult(
            scheme="https",
            netloc="discord.com",
            path=f"/api/v{self.__api_version__}/{self._endpoint}",
            query=urlencode(query_args) if query_args else "",
            fragment="",
        )
        return url.geturl()

    def _get_response(self, resp):
        if resp.content_type == "application/json":
            return resp.json()
        return resp.read()

    def _to_json(self, content: dict[str, Any]) -> str:
        return dumps(content, separators=(",", ":"), ensure_ascii=True)
