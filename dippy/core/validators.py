from attr import Attribute
from dippy.core.exceptions import MalformedDiscordToken
from re import compile
from typing import Any


discord_token_pattern = compile(r"[a-zA-Z0-9_]{24}\.[a-zA-Z0-9_]{6}\.[a-zA-Z0-9_]{27}")


def token_validator(instance: Any, field: Attribute, value: Any):
    instructions = (
        "You can find your bot's token in the Developer Portal. Click your bot application then go to the bot section "
        "on the left. Click 'Copy'. https://discord.com/developers/applications"
    )
    if not isinstance(value, str):
        raise MalformedDiscordToken(
            f"The Discord token must be a string. {instructions}"
        )

    if not discord_token_pattern.match(value.strip()):
        raise MalformedDiscordToken(
            f"The Discord token didn't look to be valid. {instructions}"
        )
