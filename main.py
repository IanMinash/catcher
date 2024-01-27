import csv
import codecs
import re

from fastapi import FastAPI, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from catcher.database import SessionLocal, engine
from catcher import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return "Greetings earthling!"


@app.get("/phrases", response_model=list[schemas.CatchPhrase])
def list_phrases(db: Session = Depends(get_db)):
    return models.CatchPhrase.get_all(db)


@app.post(
    "/phrases", status_code=status.HTTP_201_CREATED, response_model=schemas.CatchPhrase
)
def create_phrase(phrase: schemas.CatchPhraseCreate, db: Session = Depends(get_db)):
    return models.CatchPhrase(**phrase.model_dump()).create(db)


@app.get("/phrases/{id}", response_model=schemas.CatchPhrase)
def get_phrase(id: int, db: Session = Depends(get_db)):
    catch_phrase = models.CatchPhrase.get_by_id(db, id)
    if not catch_phrase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No catch phrase has been found with the given id",
        )
    return catch_phrase


@app.patch("/phrases/{id}", response_model=schemas.CatchPhrase)
def update_phrase(
    id: int, phrase: schemas.CatchPhraseCreate, db: Session = Depends(get_db)
):
    catch_phrase = models.CatchPhrase.get_by_id(db, id)
    if not catch_phrase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No catch phrase has been found with the given id",
        )
    return catch_phrase.update(db, phrase.model_dump())


@app.delete("/phrases/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_phrase(id: int, db: Session = Depends(get_db)):
    catch_phrase = models.CatchPhrase.get_by_id(db, id)
    if not catch_phrase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No catch phrase has been found with the given id",
        )
    catch_phrase.delete(db)
    return


@app.post(
    "/phrases/csv",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CatchPhraseCSVResponse,
)
def upload_phrases_csv(csv_file: UploadFile, db: Session = Depends(get_db)):
    """Expects a CSV file with the headers phrase and mapping_answer. Returns number of inserted documents"""
    reader = csv.DictReader(codecs.iterdecode(csv_file.file, "utf-8"))
    insert_records = list(reader)
    try:
        phrases = models.CatchPhrase.create_many(db, insert_records)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IntegrityError: please check the input file for duplicated",
        )
    phrases_list = phrases.all()
    return {"count": len(phrases_list)}


@app.post("/phrases/match", response_model=schemas.CatchPhrase)
def match_sentence(input: schemas.MatchSentenceRequest, db: Session = Depends(get_db)):
    # Narrow search space using the mapping_answer to filter results that we will match against.
    words = input.sentence.upper().split()
    possible_matches = (
        db.query(models.CatchPhrase)
        .filter(models.CatchPhrase.mapping_answer.in_(words))
        .all()
    )
    for possible_match in possible_matches:
        match_regexp = re.compile(rf"{possible_match.phrase}")
        if match_regexp.fullmatch(input.sentence):
            return possible_match

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No matching mapping has been found",
    )
