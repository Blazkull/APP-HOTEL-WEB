
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    from models.user import User
    from models.user_type import UserType
    from models.reservation import Reservation
    from models.reservation_status import ReservationStatus
    from models.client import Client
    from models.room import Room
    from models.room_type import RoomType
    from models.room_status import RoomStatus

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]