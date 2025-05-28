from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User

class UserType(SQLModel, table=True):
    __tablename__ = "usertype"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30,unique=True)
    description: str = Field(max_length=100)

    users: List["User"] = Relationship(back_populates="user_type")


class UserTypeBase(SQLModel):
    name: str = Field(max_length=30,unique=True)
    description: str = Field(max_length=100)

class UserTypeCreate(UserTypeBase):
    pass

class UserTypeUpdate(UserTypeBase):
    pass

class UserTypeRead(UserTypeBase):
    id: int
