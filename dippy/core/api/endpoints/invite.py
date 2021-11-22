from __future__ import annotations
from typing import Optional
from dippy.core.api.request import RequestModel, QueryArgField, URLArgField


class GetInvite(RequestModel):
    endpoint = "/invites/{invite_code}"
    method = "GET"

    invite_code: str = URLArgField()

    with_counts: Optional[bool] = QueryArgField()
    with_expiration: Optional[bool] = QueryArgField()


class DeleteInvite(URLArgField):
    endpoint = "/invites/{invite_code}"
    method = "DELETE"

    invite_code: str = URLArgField()
