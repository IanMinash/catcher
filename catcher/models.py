import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

from .database import Base


class CatchPhrase(Base):
    __tablename__ = "catch_phrases"

    id = Column(Integer, primary_key=True)
    mapping_answer = Column(String, index=True)
    phrase = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def create(self, db: Session):
        WORDCOUNT_REGEX = re.compile(r"\((\d+),(\d+)\)")
        WORD_SUB = "([A-Za-z0-9_]+ *){\\g<1>,\\g<2>}"
        self.phrase = WORDCOUNT_REGEX.sub(WORD_SUB, str(self.phrase))
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: Session):
        db.delete(self)
        return db.commit()

    def update(self, db: Session, update_fields: dict):
        for field in update_fields:
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