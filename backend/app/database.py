import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use the DATABASE_URL environment variable (RDS on AWS); fall back to SQLite locally
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# The check_same_thread option only exists for SQLite
connect_args = (
    {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
