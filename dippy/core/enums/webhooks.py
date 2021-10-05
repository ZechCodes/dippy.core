from dippy.core.enums.enums import IntEnum


class WebhookTypes(IntEnum):
    INCOMING = 1  # Incoming Webhooks can post messages to channels with a generated token
    CHANNEL_FOLLOWER = 2  # Channel Follower Webhooks are internal webhooks used with Channel Following to post new
    # messages into channels
    APPLICATION = 3  # Application webhooks are webhooks used with Interactions
