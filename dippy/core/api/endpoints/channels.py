from __future__ import annotations
from typing import Optional
from dippy.core.api.request import request_model, query_arg, url_arg
from dippy.core.snowflake import Snowflake
from dippy.core.api.models.channels import Channel


@request_model
class GetChannelRequest:
    endpoint = "/channels/{channel_id}"
    method = "GET"
    model: Channel

    channel_id: Snowflake = url_arg()


# TODO: Implement PATCH /channels/{channel.id} | Modify Channel Endpoint
#  Requires checks if a channel is a thread/DM/channel


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

    around: Optional[Snowflake] = query_arg()
    before: Optional[Snowflake] = query_arg()
    after: Optional[Snowflake] = query_arg()
    limit: Optional[int] = query_arg()


@request_model
class GetChannelMessageRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}"
    method = "GET"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()


@request_model
class CreateMessageRequest:
    endpoint = "/channels/{channel_id}/messages"
    method = "POST"

    channel_id: Snowflake = url_arg()

    # TODO: Implement https://discord.com/developers/docs/resources/channel#create-message-jsonform-params


@request_model
class CreateReactionRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    method = "PUT"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
    emoji: Snowflake = url_arg()


@request_model
class DeleteOwnReactionRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    method = "DELETE"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
    emoji: Snowflake = url_arg()


@request_model
class DeleteUserReactionRequest:
    endpoint = (
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}"
    )
    method = "DELETE"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
    emoji: Snowflake = url_arg()
    user_id: Snowflake = url_arg()


@request_model
class GetReactionsRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
    method = "DELETE"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
    emoji: Snowflake = url_arg()

    after: Optional[Snowflake] = query_arg()
    limit: Optional[int] = query_arg()


@request_model
class DeleteAllReactionsRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions"
    method = "DELETE"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()


@request_model
class DeleteAllReactionsForEmojiRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
    method = "DELETE"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()
    emoji: Snowflake = url_arg()


@request_model
class EditMessageRequest:
    endpoint = "/channels/{channel_id}/messages/{message_id}"
    method = "PATCH"

    channel_id: Snowflake = url_arg()
    message_id: Snowflake = url_arg()

    # TODO: Implement https://discord.com/developers/docs/resources/channel#edit-message-jsonform-params
