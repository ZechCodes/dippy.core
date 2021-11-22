from __future__ import annotations
from typing import Optional
from dippy.core.api.request import RequestModel, QueryArgField, URLArgField
from dippy.core.snowflake import Snowflake
from dippy.core.api.models.channels import Channel


class GetChannelRequest(RequestModel):
    endpoint = "/channels/{channel_id}"
    method = "GET"
    model: Channel

    channel_id: Snowflake = URLArgField()


# TODO: Implement PATCH /channels/{channel.id} | Modify Channel Endpoint
#  Requires checks if a channel is a thread/DM/channel


class DeleteChannelRequest(RequestModel):
    """Deletes a channel or closes a private message."""

    endpoint = "/channels/{channel_id}"
    method = "DELETE"

    channel_id: Snowflake = URLArgField()


class GetChannelMessagesRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages"
    method = "GET"

    channel_id: Snowflake = URLArgField()

    around: Optional[Snowflake] = QueryArgField()
    before: Optional[Snowflake] = QueryArgField()
    after: Optional[Snowflake] = QueryArgField()
    limit: Optional[int] = QueryArgField()


class GetChannelMessageRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}"
    method = "GET"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()


class CreateMessageRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages"
    method = "POST"

    channel_id: Snowflake = URLArgField()

    # TODO: Implement https://discord.com/developers/docs/resources/channel#create-message-jsonform-params


class CreateReactionRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    method = "PUT"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()
    emoji: Snowflake = URLArgField()


class DeleteOwnReactionRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    method = "DELETE"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()
    emoji: Snowflake = URLArgField()


class DeleteUserReactionRequest(RequestModel):
    endpoint = (
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}"
    )
    method = "DELETE"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()
    emoji: Snowflake = URLArgField()
    user_id: Snowflake = URLArgField()


class GetReactionsRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
    method = "DELETE"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()
    emoji: Snowflake = URLArgField()

    after: Optional[Snowflake] = QueryArgField()
    limit: Optional[int] = QueryArgField()


class DeleteAllReactionsRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions"
    method = "DELETE"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()


class DeleteAllReactionsForEmojiRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
    method = "DELETE"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()
    emoji: Snowflake = URLArgField()


class EditMessageRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages/{message_id}"
    method = "PATCH"

    channel_id: Snowflake = URLArgField()
    message_id: Snowflake = URLArgField()

    # TODO: Implement https://discord.com/developers/docs/resources/channel#edit-message-jsonform-params
