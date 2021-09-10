from __future__ import annotations
from typing import Optional
from dippy.core.api.request import url_arg, request_model, query_arg
from dippy.core.snowflake import Snowflake


@request_model
class GetInvite:
    endpoint = "/invites/{invite_code}"
    method = "GET"

    invite_code: str = url_arg()

    with_counts: Optional[bool] = query_arg()
    with_expiration: Optional[bool] = query_arg()


@request_model
class DeleteInvite:
    endpoint = "/invites/{invite_code}"
    method = "DELETE"

    invite_code: str = url_arg()
