from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class JobApplication(Base):
    __tablename__ = "job_applications"

    id       = Column(Integer, primary_key=True, index=True)
    company  = Column(String(200), nullable=False)
    role     = Column(String(200), nullable=False)
    status   = Column(String(50), default="Applied")
    date     = Column(String(20), nullable=False)
    location = Column(String(200), default="")
    notes    = Column(Text, default="")


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)