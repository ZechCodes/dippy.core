from dippy.core.cache.controller import (
    CacheController,
    BasicController,
    MemberController,
)
from dippy.core.exceptions import NoCacheControllerFound
from dippy.core.models.base_model import BaseModel
from dippy.core.models.guilds import Guild
from dippy.core.models.messages import Message
from dippy.core.models.users import Member, User
from typing import Any, Type, TypeVar


ModelType = TypeVar("ModelType", bound=BaseModel)


class CacheManager:
    """Manages multiple cache controllers.

    Cache controllers can be registered for any model type, the controller will then be created when it is needed. All
    get and update requests will be handed off to the appropriate controller to handle. If a controller isn't found for
    a given model type `dippy.core.exceptions.NoCacheControllerFound` will be raised.

    The base `CacheManager` registers controllers for `Guild`, `Member`, `Message`, and `User` models. This can be
    changed by calling the `add_cache_controller` method after the manager is created. Alternatively `CacheManager` can
    be subclassed and its `setup` method can be changed to add whatever cache managers are desired.
    ```python
    class CustomCacheManager(CacheManager):
        def setup(self):
            '''Use custom member cache controller'''
            super().setup()
            self.add_cache_controller(Member, CustomMemberController)
    ```
    The cache manager will look up controllers that were registered with a model type that has an overlapping MRO. So
    if the registered model type is a subclass or parent class of the requested model type it'll match. The returned
    type will always match the requested type, the cache controllers are naive and only work with dicts. The model type
    given when registering a controller only serves to distinguish the controller from other controllers registered with
    the cache manager.
    ```py
    >>> cache_manager.add_cache_controller(MyMessage, MyMessageController)
    >>> cache_manager.get(Message, 1234567)
    Message(id=1234567)
    >>> cache_manager.get(MyMessage, 1234567)
    MyMessage(id=1234567)
    ```
    This loose model behavior allows frameworks and extensions to provide their own custom models without breaking any
    third party extensions that may expect different model behavior. The underlying cached data will be shared while the
    model instances themselves are distinct.
    """

    def __init__(self):
        self._cache_controllers: dict[
            Type[ModelType], Type[CacheController[ModelType]]
        ] = {}
        self._controllers: dict[Type[ModelType], CacheController[ModelType]] = {}
        self.setup()

    def add_cache_controller(
        self, model: Type[ModelType], controller: Type[CacheController[ModelType]]
    ):
        """Adds a cache controller type to the cache manager to handle caching a given model type. An instance of the
        controller will not be created until the first time it is needed. This allows for subclasses to override the
        controllers being used without the overhead of having initialized a controller that is not going to be used.

        This method ideally shouldn't be called outside of the cache manager's `setup` method. It is however safe to
        call immediately after instantiating the manager."""
        self._cache_controllers[model] = controller

    def get(self, model: Type[ModelType], *args) -> ModelType:
        """Get's an object from the cache controller that is registered for models of the requested type. The return
        will be an instance of model, even if the controller was registered with a parent or subclass of the model. The
        model instance returned will be unique and will not be stored in the cache, the cache only stores the underlying
        data in a dict that the model then wraps. Will raise `NoCacheControllerFound` if no cache
        controller is found that matches the given model.

        :raise NoCacheControllerFound"""
        return model(self.get_cache_controller(model).get(*args))

    def get_cache_controller(
        self, model: Type[ModelType]
    ) -> CacheController[ModelType]:
        """Gets the cache controller that is registered for the given model type. The controller will be a match if the
        type it was registered with is either a parent or subclass of the requested model type. If the controller is
        found but is not yet instantiated, an instance will be created. If no cache controller is found that matches the
        requested model `NoCacheControllerFound` will be raised.

        :raise NoCacheControllerFound"""
        model_type = self._get_registered_type(model)
        if model_type not in self._controllers:
            self._controllers[model_type] = self._cache_controllers[model_type](self)
        return self._controllers[model_type]

    def setup(self):
        """Called when the cache manager is created. This is intended for registering cache controllers."""
        self.add_cache_controller(Guild, BasicController)
        self.add_cache_controller(Member, MemberController)
        self.add_cache_controller(Message, BasicController)
        self.add_cache_controller(User, BasicController)

    def update(self, model: Type[ModelType], *args, data: dict[str, Any]):
        """Updates an object in the appropriate cache controller. Will raise `NoCacheControllerFound` if no cache
        controller is found that matches the given model.

        :raise NoCacheControllerFound"""
        self.get_cache_controller(model).update(*args, data=data)

    def _get_registered_type(self, model: Type[ModelType]) -> Type[ModelType]:
        for model_type, controller_type in self._cache_controllers.items():
            if (
                issubclass(model, model_type)
                or issubclass(model_type, model)
                or model is model_type
            ):
                return model_type

        else:
            raise NoCacheControllerFound(
                f"No cache controller has been registered for models of type {model!r}"
            )
