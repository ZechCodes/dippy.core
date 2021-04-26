from __future__ import annotations
from enum import Enum
from inspect import isawaitable
from pydantic import BaseModel
from typing import Awaitable, Callable, Coroutine, Optional, Union


ModelBuilder = Union[Callable, Coroutine, BaseModel]


class MethodType(str, Enum):
    delete = "delete"
    get = "get"
    patch = "patch"
    post = "post"
    put = "put"


class Endpoint:
    def __init__(
        self,
        path: str,
        method: Union[MethodType, str] = MethodType.get,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
        setup_path: Optional[Union[Callable, Coroutine]] = None,
    ):
        self._create_request = create_request
        self._method = MethodType(method)
        self._on_result = on_result
        self._path = path
        self._setup_path = setup_path

    def __call__(self, func: ModelBuilder) -> Endpoint:
        self._create_request = func
        return self

    def __set_name__(self, owner, name):
        def caller(instance, *args, **kwargs) -> Awaitable:
            return self._make_request(instance, *args, **kwargs)

        setattr(owner, name, caller)

    def on_result(self, func: ModelBuilder) -> Endpoint:
        self._on_result = func
        return self

    def setup_path(self, func: Union[Callable, Coroutine]) -> Endpoint:
        self._setup_path = func
        return self

    async def _call(self, func, instance, *args, **kwargs):
        result = func(instance, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    async def _make_request(self, instance, *args, **kwargs):
        path_args = args, kwargs
        fields = {}
        if self._create_request:
            data: BaseModel = await self._call(
                self._create_request, instance, *args, **kwargs
            )
            fields = data.dict(exclude_none=True)
            path_args = ((data,), {})

        path = self._path
        if self._setup_path:
            path = await self._call(
                self._setup_path, instance, path, *path_args[0], **path_args[1]
            )

        request = instance.request(path)
        response, status = await getattr(request, self._method)(**fields)

        if self._on_result:
            return await self._call(self._on_result, instance, response, status)

    @classmethod
    def delete(
        cls,
        path: str,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
    ):
        return cls(path, MethodType.delete, on_result, create_request)

    @classmethod
    def get(
        cls,
        path: str,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
    ):
        return cls(path, MethodType.get, on_result, create_request)

    @classmethod
    def patch(
        cls,
        path: str,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
    ):
        return cls(path, MethodType.patch, on_result, create_request)

    @classmethod
    def post(
        cls,
        path: str,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
    ):
        return cls(path, MethodType.post, on_result, create_request)

    @classmethod
    def put(
        cls,
        path: str,
        on_result: Optional[ModelBuilder] = None,
        create_request: Optional[ModelBuilder] = None,
    ):
        return cls(path, MethodType.put, on_result, create_request)
