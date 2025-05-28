from decimal import Decimal
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.room_type import RoomType
    from models.room_status import RoomStatus

class RoomBase(SQLModel):
    room_number: str = Field(max_length=30,unique=True)
    price_per_night: Decimal
    capacity: int = Field(default=1)
    room_type_id: int = Field(foreign_key="roomtype.id")
    room_status_id: int = Field(foreign_key="roomstatus.id")
    active:bool =Field(default=True)
    
class Room(RoomBase, table=True):
    __tablename__ = "room"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    active:bool =Field(default=True)

    reservations: List["Reservation"] = Relationship(back_populates="room")
    room_type: Optional["RoomType"] = Relationship(back_populates="rooms") # name update
    room_status: Optional["RoomStatus"] = Relationship(back_populates="rooms") # nombre y back populate update

class RoomCreate(RoomBase):
    pass

class RoomUpdate(SQLModel):
    room_number: Optional[str] = Field(default=None, max_length=30)
    price_per_night: Optional[Decimal] = None
    capacity: Optional[int] = Field(default=None)
    room_type_id: Optional[int] = Field(default=None, foreign_key="roomtype.id")
    room_status_id: Optional[int] = Field(default=None, foreign_key="roomstatus.id")
    active:bool =Field(default=True)

class RoomRead(RoomBase):
    id: int

class RoomStatusUpdate(SQLModel):
    active: Optional[bool] = Field(default=True)