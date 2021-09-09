from attr import Attribute
from dippy.core.exceptions import MalformedDiscordToken
from re import compile
from typing import Any


discord_token_pattern = compile(
    r"[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}"
)


def token_validator(instance: Any, field: Attribute, value: Any):
    instructions = (
        "You can find your bot's token in the Developer Portal. Click your bot application then go to the bot section "
        "on the left. Click 'Copy'. https://discord.com/developers/applications"
    )
    if not value:
        value_name = {None: "None", "": "an empty string"}
        raise MalformedDiscordToken(
            f"The Discord Token provided was {value_name}. If you're reading the token from the local environment, "
            f"ensure the token is set and that you're using the correct environment variable name."
        )
    if not isinstance(value, str):
        raise MalformedDiscordToken(
            f"The Discord Token provided must be a string. {instructions}"
        )

    if not discord_token_pattern.match(value.strip()):
        raise MalformedDiscordToken(
            f"The Discord Token provided isn't valid. {instructions}"
        )
