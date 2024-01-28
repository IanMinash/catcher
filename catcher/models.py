import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

from .database import Base


class CatchPhrase(Base):
    __tablename__ = "catch_phrases"

    WORDCOUNT_REGEX = re.compile(r"[ ]?\( *(\d+) *, *(\d+) *\)[ ]?")
    WORD_SUB = "( *[A-Za-z0-9_]+ *){\\g<1>,\\g<2>}"

    id = Column(Integer, primary_key=True)
    mapping_answer = Column(String, index=True)
    phrase = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"[{self.mapping_answer}] {self.phrase}"

    def create(self, db: Session):
        self.phrase = self.WORDCOUNT_REGEX.sub(self.WORD_SUB, str(self.phrase))
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def create_many(cls, db: Session, catch_phrases: list[dict]):
        from sqlalchemy import insert

        catch_phrases = [
            {
                "mapping_answer": phrase["mapping_answer"],
                "phrase": cls.WORDCOUNT_REGEX.sub(cls.WORD_SUB, phrase["phrase"]),
            }
            for phrase in catch_phrases
        ]
        result = db.execute(insert(cls).returning(cls), catch_phrases)
        db.commit()
        return result

    def delete(self, db: Session):
        db.delete(self)
        return db.commit()

    def update(self, db: Session, update_fields: dict):
        for field in update_fields:
            if field == "phrase":
                update_fields[field] = self.WORDCOUNT_REGEX.sub(
                    self.WORD_SUB, update_fields[field]
                )
            setattr(self, field, update_fields[field])
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def get_by_id(cls, db: Session, id: int):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_all(cls, db: Session, filters: dict = None):
        filterset = []
        if filters:
            for k in filters:
                filterset.append(getattr(cls, k) == filters[k])
        return db.query(cls).filter(*filterset).all()
