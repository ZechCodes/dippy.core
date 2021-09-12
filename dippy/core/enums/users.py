from dippy.core.enums.enums import StrEnum


class Status(StrEnum):
    IDLE = "idle"
    DND = "dnd"
    ONLINE = "online"
    OFFLINE = "offline"
