from dippy.core.models.emoji import EmojiModel
from dippy.core.models.model import DippyCoreModel


class ReactionModel(DippyCoreModel):
    count: int
    me: bool
    emoji: EmojiModel
