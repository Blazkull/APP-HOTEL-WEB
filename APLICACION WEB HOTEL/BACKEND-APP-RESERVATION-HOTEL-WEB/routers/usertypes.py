from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select

from models.user_type import UserType, UserTypeCreate, UserTypeUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de usuario
@router.get("/api/usertypes", response_model=list[UserType], tags=["USER TYPES"])
def list_usertype(session: SessionDep):
    try:
        return session.exec(select(UserType)).all()#esto ejecuta transacciones de sql
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"this list usertype doesn´t: {str(e)}",
        )


# obtener tipo de usuario por id para listar
@router.get("/api/usertypes/{usertype_id}", response_model=UserType, tags=["USER TYPES"])
def read_usertype(usertype_id: int, session: SessionDep):
    try:   
        usertype_db = session.get(UserType, usertype_id)
        if not usertype_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Type doesn't exits"
            )#status.http y el codigo y detail es para el mensaje que retorna
        return usertype_db


    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting user type: {str(e)}",
        )


#crear tipo de usuario
@router.post("/api/usertypes", response_model=UserType, status_code=status.HTTP_201_CREATED ,tags=["USER TYPES"])
def create_user(user_type_data: UserTypeCreate,session: SessionDep):

    try:
        #validate
        usertype = UserType.model_validate(user_type_data.model_dump())
        existing_user_type=session.exec(select(UserType).where(UserType.name == usertype.name)).first()
        if existing_user_type:
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="User Type already registered" 
            )
        session.add(usertype)#insertamos datos
        session.commit()#conectamos la bd
        session.refresh(usertype)#refrescamos despues de insertar datos
        return usertype

    except HTTPException as http_exc:
    # Re-raise HTTPExceptions to avoid them being caught by the general Exception handler
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating user type: {str(e)}",
        )



# obtener user_types por id para eliminar
@router.delete("/api/usertypes/{usertype_id}",status_code=status.HTTP_200_OK, tags=["USER TYPES"])
def delete_usertype(usertype_id: int, session: SessionDep):

    try:
        usertype_db = session.get(UserType, usertype_id)
        if not usertype_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="UserType doesn´t exist"
            )
        session.delete(usertype_db)
        session.commit()
        return {"detail": "user type deleted succesfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting user type: {str(e)}",
        )


# obtener tipo de usuario por id para actualizar
@router.patch("/api/usertypes/{usertype_id}", response_model=UserType, tags=["USER TYPES"])
def update_usertype( usertype_id: int, usertype_data: UserTypeUpdate, session: SessionDep):

    try:
        usertype_db = session.get(UserType, usertype_id)
        #validate
        if not usertype_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User type doesn't exits"
            )
        usertype_data_dict=usertype_data.model_dump(exclude_unset=True)
        #validador
        if "name" in usertype_data_dict and usertype_data_dict["name"] != usertype_db.name:
            existing_usertype = session.exec(select(UserType).where(UserType.name == usertype_data_dict["username"])).first()
            if existing_usertype and existing_usertype.id != usertype_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
                )
        usertype_db.sqlmodel_update(usertype_data_dict)
        session.add(usertype_db)
        session.commit()
        session.refresh(usertype_db)
        return usertype_db

    except HTTPException as http_exc:
    # Re-raise HTTPExceptions to avoid them being caught by the general Exception handler
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating user type: {str(e)}",
        )
    

    