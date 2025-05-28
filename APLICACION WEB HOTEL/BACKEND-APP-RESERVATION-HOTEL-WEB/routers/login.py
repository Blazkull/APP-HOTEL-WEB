from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from core.database import SessionDep
from models.user import User, LoginRequest, UserLogin

router = APIRouter()

@router.post("/api/login", response_model=UserLogin, tags=["AUTH"])
def login(login_data: LoginRequest, session: SessionDep):
    try:
        user_db = session.exec(select(User).where(User.username == login_data.username)).first()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user_db.password != login_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        return {
            "message": f"Bienvenido, {user_db.username}!",
            "username": user_db.username,
            "user_type_id": user_db.user_type_id  # ✅ correcto campo
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}",
        )
