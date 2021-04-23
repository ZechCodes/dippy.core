from pydantic import BaseModel, validator


class DippyCoreModel(BaseModel):
    @validator(
        "team_id",
        "owner_user_id",
        "primary_sku_id",
        "guild_id",
        "id",
        pre=True,
        allow_reuse=True,
    )
    def convert_id_to_int(cls, value):
        return int(value) if value is not None else value
