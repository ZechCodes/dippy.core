from dippy.core.cache.manager import CacheManager
from dippy.core.cache.controller import BasicController
from dippy.core.models.base_model import BaseModel
from dippy.core.snowflake import Snowflake
from pytest import fixture
from typing import Type


@fixture()
def model():
    class Model(BaseModel):
        def __init__(self, data):
            self.data = data

    return Model


@fixture()
def model_b():
    class ModelB(BaseModel):
        def __init__(self, data):
            self.data = data

    return ModelB


@fixture()
def controller():
    class Controller(BasicController):
        def __init__(self, manager):
            super().__init__(manager)
            self._cache.update(
                {Snowflake(0): {"name": "Hello"}, Snowflake(1): {"name": "World"}}
            )

    return Controller


@fixture()
def manager(controller, model, model_b):
    class Manager(CacheManager):
        def setup(self):
            self.add_cache_controller(model, controller)
            self.add_cache_controller(model_b, controller)

    return Manager


def test_cache_controller(manager, model):
    m = manager()
    value = m.get(model, 1)
    assert value.data == {"name": "World"}


def test_multiple_caches(
    manager: Type[CacheManager], model: Type[BaseModel], model_b: Type[BaseModel]
):
    m = manager()
    m.update(model, 1, data={"name": "WORLD"})
    v1, v2 = m.get(model, 1), m.get(model_b, 1)
    assert (v1.data["name"], v2.data["name"]) == ("WORLD", "World")
