from __future__ import annotations
from aiohttp import ClientSession
from asyncio import AbstractEventLoop, get_running_loop
from bevy import Context, Inject
from dippy.core.api.request import RequestModel
from dippy.core.cache.manager import CacheManager
from dippy.core.model.data_models import DataModel
from dippy.core.model.fields import Field
from dippy.core.model.models import Model
from dippy.core.validators import token_validator
from typing import Any, Optional, Type, Union
import urllib.parse


class ClientProxy(DataModel):
    proxy: Optional[str] = None
    proxy_auth: Optional[object] = None
    proxy_headers: Optional[dict[str, Any]] = None


class DiscordRestClient(DataModel):
    __api_version__ = 9
    cache: CacheManager = Inject(CacheManager)

    token: str = Field(converter=str.strip, default="", validator=token_validator)
    client_name: str = Field(converter=str.strip, default="dippy.core", kw_only=True)
    loop: AbstractEventLoop = Field(factory=get_running_loop, kw_only=True)
    headers: dict[str, Any] = Field(factory=dict, kw_only=True)
    proxy: Optional[ClientProxy] = Field(factory=ClientProxy, kw_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session: Optional[ClientSession] = None

    async def __aenter__(self) -> DiscordRestClient:
        self._session = self._create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    def create_model(self, request: RequestModel, response: dict[str, Any]):
        if isinstance(request.model, type) and issubclass(request.model, Model):
            return self._create_with_cache(request.model, response)

        return request.model(**response)

    async def request(
        self, request: RequestModel
    ) -> Union[Model, Type, dict[str, Any]]:
        response = await self._make_request(
            request.method,
            self._build_url(request),
            self._get_query_args(request),
            self._get_json_args(request),
        )
        return self.create_model(request, response)

    def _build_url(self, request: RequestModel) -> str:
        url = f"https://discord.com/api/v{self.__api_version__}/{request.endpoint.lstrip('/')}"
        return url.format(**self._get_url_args(request))

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

    def _create_with_cache(self, model, request: BaseRequest, response: dict[str, Any]):
        index = (
            request.get_index(response)
            if hasattr(request, "get_index")
            else (response["id"],)
        )
        self.cache.update(model, *index, data=response)
        return self.cache.get(model, *index)

    def _get_json_args(self, request: BaseRequest) -> dict[str, Any]:
        return asdict(
            request,
            filter=lambda attr, value: (
                attr.metadata.get("arg_type") == "json" and value is not NOT_SET
            ),
            value_serializer=lambda inst, attr, value: str(value),
        )

    def _get_query_args(self, request: BaseRequest) -> dict[str, Any]:
        return asdict(
            request,
            filter=lambda attr, value: (
                attr.metadata.get("arg_type") == "query" and value is not NOT_SET
            ),
            value_serializer=lambda inst, attr, value: str(value),
        )

    def _get_url_args(self, request: BaseRequest) -> dict[str, Any]:
        return asdict(
            request,
            filter=lambda attr, value: attr.metadata.get("arg_type") == "url",
            value_serializer=lambda inst, attr, value: urllib.parse.unquote(str(value)),
        )

    async def _make_request(
        self,
        method: str,
        url: str,
        query_args: Optional[dict] = None,
        json_args: Optional[dict] = None,
    ) -> dict[str, Any]:
        kwargs = {**asdict(self.proxy)}
        if query_args:
            kwargs["params"] = query_args
        if json_args:
            kwargs["json"] = json_args
        response = await self._session.request(method, url, **kwargs)
        json = await response.json()
        return json

    @classmethod
    def connect(cls, token: str, **kwargs) -> DiscordRestClient:
        context = Context()
        client = context.build(DiscordRestClient, token, **kwargs)
        context.add(client)
        return client
