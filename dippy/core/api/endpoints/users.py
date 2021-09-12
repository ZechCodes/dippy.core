from __future__ import annotations
from dippy.core.api.request import request_model, url_arg
from dippy.core.models.users import User
from dippy.core.snowflake import Snowflake


@request_model
class GetUser:
    endpoint = "/users/{user_id}"
    method = "GET"
    model = User

    user_id: Snowflake = url_arg()
