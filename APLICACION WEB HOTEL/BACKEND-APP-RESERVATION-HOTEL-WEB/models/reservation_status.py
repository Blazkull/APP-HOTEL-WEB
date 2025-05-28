from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class ReservationStatus(SQLModel, table=True):
    __tablename__ = "reservationstatus"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30,unique=True)
    description: str = Field(max_length=100)

    reservations: List["Reservation"] = Relationship(back_populates="reservation_status") 


class ReservationStatusBase(SQLModel):
    name: str = Field(max_length=30)
    description: str = Field(max_length=100)

class ReservationStatusCreate(ReservationStatusBase):
    pass

class ReservationStatusUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=30)
    description: Optional[str] = Field(default=None, max_length=100)

class ReservationStatusRead(ReservationStatusBase):
    id: int


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.reservation import Reservation
