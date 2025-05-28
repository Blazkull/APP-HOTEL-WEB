from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.room import Room

class RoomType(SQLModel, table=True):
    __tablename__ = "roomtype"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    description: str = Field(max_length=100)

    rooms: List["Room"] = Relationship(back_populates="room_type")


class RoomTypeBase(SQLModel):
    name: str = Field(max_length=30)
    description: str = Field(max_length=100)

class RoomTypeCreate(RoomTypeBase):
    pass

class RoomTypeUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=30)
    description: Optional[str] = Field(default=None, max_length=100)

class RoomTypeRead(RoomTypeBase):
    id: int
