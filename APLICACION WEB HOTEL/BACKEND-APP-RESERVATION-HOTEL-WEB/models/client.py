from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr



class Client(SQLModel, table=True):
    __tablename__ = "client"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=20,unique=True)
    email: EmailStr = Field(max_length=100,unique=True)
    number_identification: str = Field(max_length=30,unique=True)
    active:bool =Field(default=True)

    reservations: List["Reservation"] = Relationship(back_populates="client")


class ClientBase(SQLModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=20,unique=True)
    email: EmailStr = Field(max_length=100,unique=True)
    number_identification: str = Field(max_length=30,unique=True)
    active:bool =Field(default=True)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int

class ClientStatus(SQLModel):
    active: Optional[bool] = Field(default=True)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.reservation import Reservation