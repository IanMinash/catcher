from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    catch_phrase.update(db, phrase)


@app.delete("/phrases/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_phrase(id: int, db: Session = Depends(get_db)):
    catch_phrase = models.CatchPhrase.get_by_id(db, id)
    if not catch_phrase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No catch phrase has been found with the given id",
        )
    catch_phrase.delete()
    return
