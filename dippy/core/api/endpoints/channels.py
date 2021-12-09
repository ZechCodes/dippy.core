from __future__ import annotations
from typing import Optional
from dippy.core.model.partials import Partial
from dippy.core.api.request import (
    RequestModel,
    JSONArgField,
    QueryArgField,
    URLArgField,
)
from dippy.core.snowflake import Snowflake
from dippy.core.api.models.channels import Channel
from dippy.core.api.models.messages import (
    AllowedMentions,
    Component,
    Embed,
    Message,
    MessageReference,
)


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


class AttachmentPartial(Partial):
    id: Snowflake


class CreateMessageRequest(RequestModel):
    endpoint = "/channels/{channel_id}/messages"
    method = "POST"
    model = Message

    channel_id: Snowflake = URLArgField()

    content: Optional[str] = JSONArgField(kw_only=True)
    embeds: Optional[list[Embed]] = JSONArgField(kw_only=True)
    sticker_ids: Optional[list[Snowflake]] = JSONArgField(kw_only=True)
    files: Optional[list[bytes]] = JSONArgField(kw_only=True)

    tts: Optional[bool] = JSONArgField(kw_only=True)
    allowed_mentions: Optional[AllowedMentions] = JSONArgField(kw_only=True)
    message_reference: Optional[MessageReference] = JSONArgField(kw_only=True)
    components: Optional[list[Component]] = JSONArgField(kw_only=True)
    payload_json: Optional[str] = JSONArgField(kw_only=True)
    attachments: Optional[AttachmentPartial] = JSONArgField(kw_only=True)


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
