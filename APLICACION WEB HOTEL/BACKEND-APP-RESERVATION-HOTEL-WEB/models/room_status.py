from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.room import Room

class RoomStatus(SQLModel, table=True):
    __tablename__ = "roomstatus"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    description: str = Field(max_length=100)

    rooms: List["Room"] = Relationship(back_populates="room_status") #---

class RoomStatusBase(SQLModel):
    name: str = Field(max_length=30)
    description: str = Field(max_length=100)

class RoomStatusCreate(RoomStatusBase):
    pass

class RoomStatusUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=30)
    description: Optional[str] = Field(default=None, max_length=100)

class RoomStatusRead(RoomStatusBase):
    id: int