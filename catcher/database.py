from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

SQLALCHEMY_DATABASE_URL = config("DB_URL", default="sqlite:///./catcher.sqlite")

connection_arguments = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connection_arguments["check_same_thread"] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connection_arguments,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
