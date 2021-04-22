from pydantic import BaseModel, Field
from typing import Optional, Union


class Payload(BaseModel):
    op_code: int = Field(alias="op")
    sequence_num: Optional[int] = Field(None, alias="s")
    event: Optional[str] = Field("", alias="t")
    data: Optional[Union[list, dict]] = Field(None, alias="d")
