from dippy.core.enums.enums import IntEnum, IntFlag


class ActivityType(IntEnum):
    Game = 0  # Playing {name} - Example: "Playing Rocket League"
    Streaming = 1  # Streaming {details} - Example: "Streaming Rocket League"
    Listening = 2  # Listening to {name} - Example: "Listening to Spotify"
    Watching = 3  # Watching {name} - Example: "Watching YouTube Together"
    Custom = 4  # {emoji} {name} - Example: ":smiley: I am cool"
    Competing = 5  # Competing in {name} - Example: "Competing in Arena World Champions"


class ActivityFlag(IntFlag):
    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5
