from __future__ import annotations
from dippy.core.api.request import request_model, query_arg, url_arg
from dippy.core.snowflake import Snowflake


@request_model
class GetChannelRequest:
    endpoint = "/channels/{channel_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()

# TODO: Implement PATCH /channels/{channel.id}


@request_model
class DeleteChannelRequest:
    """Deletes a channel or closes a private message."""
    endpoint = "/channels/{channel_id}"
    method = "DELETE"

    channel_id: Snowflake = url_arg()


@request_model
class GetChannelMessagesRequest:
    endpoint = "/channels/{channel_id}/messages"
    method = "GET"

    channel_id: Snowflake = url_arg()

    around: Snowflake = query_arg()
    before: Snowflake = query_arg()
    after: Snowflake = query_arg()
    limit: Snowflake = query_arg()


@request_model
class GetChannelMessageRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
