from datetime import datetime

from pydantic import BaseModel


class CatchPhraseBase(BaseModel):
    mapping_answer: str
    phrase: str


class CatchPhraseCreate(CatchPhraseBase):
    pass


class CatchPhrase(CatchPhraseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
