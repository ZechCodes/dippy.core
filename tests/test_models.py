from dippy.core.model import Field, Model
from dippy.core.snowflake import Snowflake
from pytest import raises
from typing import Optional


def test_model():
    class TestModel(Model):
        id: Snowflake
        name: str
        enabled: bool = False

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
        name: str = Field(immutable=True)

    t = TestModel({"name": "Bob"})

    with raises(AttributeError):
        t.name = "kaboom"


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
