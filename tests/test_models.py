from dippy.core.datetime_helpers import datetime, now
from dippy.core.models.base_model import BaseModel
from dippy.core.snowflake import Snowflake


def test_model():
    class TestModel(BaseModel):
        id: Snowflake
        name: str
        enabled: bool = False

    t = TestModel({"id": 1234567890, "name": "Bob"})

    assert Snowflake(1234567890) == t.id
    assert t.name == "Bob"
