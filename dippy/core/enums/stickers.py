from dippy.core.enums.enums import IntEnum


class StickerType(IntEnum):
    STANDARD = 1  # an official sticker in a pack, part of Nitro or in a removed purchasable pack
    GUILD = 2  # a sticker uploaded to a Boosted guild for the guild's members


class StickerFormatType(IntEnum):
    PNG = 1
    APNG = 2
    LOTTIE = 3
