from __future__ import annotations
from aiohttp import ClientSession
from asyncio import AbstractEventLoop, get_running_loop
from bevy import Context, Inject
from dataclasses import asdict, dataclass
from dippy.core.api.request import RequestModel
from dippy.core.cache.manager import CacheManager
from dippy.core.model.data_models import DataModel
from dippy.core.model.fields import Field
from dippy.core.model.models import Model
from dippy.core.validators import token_validator
from typing import Any, Optional, Type, TypeVar, Union


T = TypeVar("T", bound=Model)


@dataclass
class ClientProxy:
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

    def create_model(self, request: RequestModel[T], response: dict[str, Any]) -> T:
        if isinstance(request.model, type) and issubclass(request.model, Model):
            return self._create_with_cache(request, response)

        return request.model(**response) if request.model else response

    async def request(self, request: RequestModel[T]) -> T:
        response = await self._make_request(request)
        return self.create_model(request, response)

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

    def _create_with_cache(self, request: RequestModel, response: dict[str, Any]):
        self.cache.update(request.model, response, *request.__dippy_index__)
        return self.cache.get(request.model, *request.__dippy_index__)

    async def _make_request(self, request: RequestModel[T]) -> dict[str, Any]:
        kwargs = asdict(self.proxy)
        if request.query_args:
            kwargs["params"] = {
                key: str(value) if isinstance(value, bool) else value
                for key, value in request.query_args.items()
                if value is not None
            }
        if request.json_args:
            kwargs["json"] = {
                key: value
                for key, value in request.json_args.items()
                if value is not None
            }
        response = await self._session.request(
            request.method, request.get_url(self.__api_version__), **kwargs
        )
        json = await response.json()
        return json

    @classmethod
    def connect(cls, token: str, **kwargs) -> DiscordRestClient:
        context = Context()
        client = context.build(DiscordRestClient, token, **kwargs)
        context.add(client)
        return client
