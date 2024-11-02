from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from prometheus_fastapi_instrumentator import Instrumentator
from kafka import KafkaProducer
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel

app = FastAPI()
load_dotenv()

# Database settings
DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Kafka producer configuration
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

Instrumentator().instrument(app).expose(app)


class UserCreate(BaseModel):
    user_name: str
    email: str


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/register/",
    tags=["Users"],
    description="Register a new user and store it in MySQL, then emit a UserRegistered event.",
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and store it in MySQL, then emit a UserRegistered event."""
    new_user = User(name=user.user_name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    event = {
        "event_type": "UserRegistered",
        "data": {"user_name": user.user_name, "email": user.email},
    }
    producer.send("user_events", event)

    return {"message": "User registered successfully"}


@app.get("/user-service", tags=["Root"])
async def root():
    return {"message": "User Service - OK"}
