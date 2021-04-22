from enum import IntEnum as _IntEnum


__all__ = ["Intents"]


class Intents(_IntEnum):
    BANS = 1 << 2
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    EMOJIS = 1 << 3
    GUILDS = 1 << 0
    INTEGRATIONS = 1 << 4
    INVITES = 1 << 6
    MEMBERS = 1 << 1
    MESSAGES = 1 << 9
    MESSAGE_REACTIONS = 1 << 10
    MESSAGE_TYPING = 1 << 11
    PRESENCES = 1 << 8
    VOICE_STATES = 1 << 7
    WEBHOOKS = 1 << 5

    DEFAULT = (
        GUILDS
        | BANS
        | EMOJIS
        | INTEGRATIONS
        | WEBHOOKS
        | INVITES
        | VOICE_STATES
        | MESSAGES
        | MESSAGE_REACTIONS
        | MESSAGE_TYPING
        | DIRECT_MESSAGES
        | DIRECT_MESSAGE_REACTIONS
        | DIRECT_MESSAGE_TYPING
    )

    bans = BANS
    default = DEFAULT
    direct_message_reactions = DIRECT_MESSAGE_REACTIONS
    direct_message_typing = DIRECT_MESSAGE_TYPING
    direct_messages = DIRECT_MESSAGES
    emojis = EMOJIS
    guilds = GUILDS
    integrations = INTEGRATIONS
    invites = INVITES
    members = MEMBERS
    message_reactions = MESSAGE_REACTIONS
    message_typing = MESSAGE_TYPING
    messages = MESSAGES
    presences = PRESENCES
    voice_states = VOICE_STATES
    webhooks = WEBHOOKS
