from dippy.core.snowflake import Snowflake
from dippy.core.datetime_helpers import from_timestamp


def test_snowflake_datetime():
    assert Snowflake(644299523686006834).timestamp == from_timestamp(1573683376.953)


def test_snowflake_worker_id():
    assert Snowflake(644299523686006834).worker_id == 1


def test_snowflake_process_id():
    assert Snowflake(644299523686006834).process_id == 0


def test_snowflake_increment():
    assert Snowflake(644299523686006834).increment == 50
