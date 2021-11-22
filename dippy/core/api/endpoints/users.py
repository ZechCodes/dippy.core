from __future__ import annotations
from dippy.core.api.request import RequestModel, URLArgField
from dippy.core.api.models.users import User
from dippy.core.snowflake import Snowflake


class GetUser(RequestModel):
    endpoint = "/users/{id}"
    method = "GET"
    model = User

    id: Snowflake = URLArgField(index=True, key_name="user_id")
