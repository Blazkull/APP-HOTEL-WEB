from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    reservation_status_id:int = Field(foreign_key="reservationstatus.id")
    client_id : int = Field(foreign_key="client.id")
    room_id : int = Field(foreign_key="room.id")
    check_in_date: date
    check_out_date: date
    note: str = Field(max_length=100)
    total: Decimal = Field(default=Decimal(0.00))

    user: Optional["User"] = Relationship(back_populates="reservations")
    reservation_status : Optional["ReservationStatus"] = Relationship(back_populates="reservations") 
    client: Optional["Client"] = Relationship(back_populates="reservations")
    room: Optional["Room"] = Relationship(back_populates="reservations")


class ReservationBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    reservation_status_id: int = Field(foreign_key="reservationstatus.id")
    client_id: int = Field(foreign_key="client.id")
    room_id: int = Field(foreign_key="room.id")
    check_in_date: date
    check_out_date: date  # Assuming this is the check-out date based on context
    note: str = Field(max_length=100)
    total: Decimal = Field(default=Decimal(0.00))

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int

    class Config:
        from_attributes = True

class ReservationUpdate(SQLModel):
    user_id: Optional[int] = None
    reservation_status_id: Optional[int] = None
    client_id: Optional[int] = None
    room_id: Optional[int] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    note: Optional[str] = None
    total: Optional[Decimal] = None

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.reservation_status import ReservationStatus
    from models.client import Client
    from models.room import Room
