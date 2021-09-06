from __future__ import annotations
from aiohttp import ClientSession
from asyncio import AbstractEventLoop, get_running_loop
from attr import asdict, attrs, attrib, setters
from dippy.core.api.request import BaseRequest, NOT_SET
from dippy.core.validators import token_validator
from typing import Any, Optional
import urllib.parse


@attrs(auto_attribs=True, on_setattr=setters.frozen)
class ClientProxy:
    proxy: Optional[str] = None
    proxy_auth: Optional[object] = None
    proxy_headers: Optional[dict[str, Any]] = None


@attrs(auto_attribs=True, on_setattr=setters.frozen)
class DiscordRestClient:
    __api_version__ = 9
    token: str = attrib(converter=str.strip, default="", validator=token_validator)
    client_name: str = attrib(converter=str.strip, default="dippy.core", kw_only=True)
    loop: AbstractEventLoop = attrib(factory=get_running_loop, kw_only=True)
    headers: dict[str, Any] = attrib(factory=dict, kw_only=True)
    proxy: Optional[ClientProxy] = attrib(factory=ClientProxy, kw_only=True)

    def __attrs_post_init__(self):
        self._session: Optional[ClientSession] = None

    async def __aenter__(self) -> DiscordRestClient:
        self._session = self._create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def request(self, request: BaseRequest) -> dict[str, Any]:
        url = self._build_url(request)
        return await self._make_request(request.method, url)

    def _build_url(self, request: BaseRequest) -> str:
        url = f"https://discord.com/api/v{self.__api_version__}/{request.endpoint.lstrip('/')}"
        url = url.format(**self._get_url_args(request))
        url += self._build_query_args(request)
        return url

    def _build_query_args(self, request: BaseRequest):
        args = self._get_query_args(request)
        return f"?{urllib.parse.urlencode(args)}" if args else ""

    def _create_user_agent(self):
        from dippy.core.version import (
            __aiohttp_version__,
            __python_version__,
            __version__,
        )

        repo = "https://github.com/ZechCodes/dippy.core"
        return f"{self.client_name} ({repo}, {__version__}), Python/{__python_version__}, aiohttp/{__aiohttp_version__}"

    def _create_session(self) -> ClientSession:
        headers = self.headers.copy()
        headers.setdefault("X-Ratelimit-Precision", "millisecond")
        headers.update(
            {
                "Authorization": f"Bot {self.token}",
                "User-Agent": self._create_user_agent(),
            }
        )
        return ClientSession(headers=headers)

    def _get_query_args(self, request: BaseRequest) -> dict[str, Any]:
        return asdict(
            request,
            filter=lambda attr, value: (
                attr.metadata.get("query_arg", False) and value is not NOT_SET
            ),
            value_serializer=lambda inst, attr, value: str(value),
        )

    def _get_url_args(self, request: BaseRequest) -> dict[str, Any]:
        return asdict(
            request,
            filter=lambda attr, value: not attr.metadata.get("query_arg", False),
            value_serializer=lambda inst, attr, value: urllib.parse.unquote(str(value)),
        )

    async def _make_request(self, method: str, url: str) -> dict[str, Any]:
        response = await self._session.request(method, url, **asdict(self.proxy))
        json = await response.json()
        return json
