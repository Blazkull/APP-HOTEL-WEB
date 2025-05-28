from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(max_length=30,unique=True)
    email: EmailStr = Field(max_length=100,unique=True)
    password: str = Field(max_length=100)
    user_type_id: int = Field(foreign_key="usertype.id") 

class User(UserBase, table=True):
    __tablename__ = "user"  # Nombre de tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    active:bool =Field(default=True)
    

    reservations: List["Reservation"] = Relationship(back_populates="user")
    user_type: Optional["UserType"] = Relationship(back_populates="users")

class UserLogin(SQLModel):
    username: str = Field(max_length=30)
    email: EmailStr = Field(max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)
    active:bool =Field(default=True)

class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=100)
    user_type_id: Optional[int] = None
    active: Optional[bool] = Field(default=True)

class UserRead(UserBase):
    id: int


class Login(UserBase):
   username: str = Field(max_length=30)
   password: str = Field(max_length=100)

# En models/user.py
class LoginRequest(SQLModel):
    username: str
    password: str

# En models/user.py
class UserLogin(SQLModel):
    message: str
    username: str
    user_type_id: int



class PasswordUpdate(SQLModel):
    password: str = Field(max_length=100)

class UserStatus(SQLModel):
    active: Optional[bool] = Field(default=True)
   
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.user_type import UserType