from bevy import Context
from dippy.core.cache.manager import CacheManager
from dippy.core.model.fields import Field
from dippy.core.model.models import Model
from dippy.core.api.models.channels import Channel
from dippy.core.snowflake import Snowflake
from pytest import fixture, raises
from typing import Optional


@fixture
def context():
    return Context()


@fixture
def cache(context):
    cache_manager = context.build(CacheManager)
    context.add(cache_manager)
    return cache_manager


def test_model():
    class TestModel(Model):
        id: Snowflake
        name: str = Field(assignable=True)
        enabled: bool = Field(default=False, assignable=True)

    t = TestModel({"id": 1234567890, "name": "Bob"})

    assert Snowflake(1234567890) == t.id
    assert isinstance(t.id, Snowflake)
    assert t.name == "Bob"
    assert t.enabled is False

    t.enabled = True
    assert t.enabled

    t.name = 1337
    assert isinstance(t.name, str)
    assert t.name == "Bob"


def test_model_immutable_fields():
    class TestModel(Model):
        name: str

    t = TestModel({"name": "Bob"})

    with raises(AttributeError):
        t.name = "kaboom"

    class TestModel(Model):
        name: str = Field(assignable=True)

    t = TestModel({"name": "Bob"})
    t.name = "nothing_burger"
    assert t.name == "nothing_burger"


def test_model_optional():
    class TestModel(Model):
        id: Optional[Snowflake]

    t = TestModel({"id": 1234567890})

    assert isinstance(t.id, Snowflake)

    t = TestModel({})

    assert t.id is None


def test_model_indexes():
    class TestModel(Model):
        id: Snowflake = Field(index=True)
        name: str = "Bob"

    t = TestModel({"id": 1234567890})

    assert t.__dippy_index__ == (Snowflake(1234567890),)

    class TestModel(Model):
        id: Snowflake = Field(index=True)
        name: str = Field(default="Bob", index=True)

    t = TestModel({"id": 1234567890})

    assert t.__dippy_index__ == (Snowflake(1234567890), "Bob")


def test_channel_model(cache):
    cache.update(Channel, {"id": 1, "name": "Test Channel"})
    channel = cache.get(Channel, 1)
    assert channel.name == "Test Channel"
