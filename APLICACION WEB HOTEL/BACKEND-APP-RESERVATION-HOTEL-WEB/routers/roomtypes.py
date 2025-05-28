from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select

from models.room_type import RoomType, RoomTypeCreate, RoomTypeUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de habitacion
@router.get("/api/roomtypes", response_model=list[RoomType], tags=["ROOM TYPES"])
def list_roomtype(session: SessionDep):
    return session.exec(select(RoomType)).all()#esto ejecuta transacciones de sql


# obtener tipo de habitacion por id para listar
@router.get("/api/roomtypes/{roomtype_id}", response_model=RoomType, tags=["ROOM TYPES"])
def read_roomtype(roomtype_id: int, session: SessionDep):

    try:
        roomtype_db = session.get(RoomType, roomtype_id)
        if not roomtype_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
            )#status.http y el codigo y detail es para el mensaje que retorna
        return roomtype_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"this list usertype doesn´t: {str(e)}",
        )

#crear tipo de habitacion
@router.post("/api/roomtypes", response_model=RoomType,status_code=status.HTTP_201_CREATED,tags=["ROOM TYPES"])
def create_roomtype(room_types_data: RoomTypeCreate,session: SessionDep):
    try:
        #validate
        roomtype = RoomType.model_validate(room_types_data.model_dump())
        existing_user_type=session.exec(select(RoomType).where(RoomType.name == roomtype.name)).first()
        if existing_user_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User Type already registered" 
            )
        session.add(roomtype)#insertamos datos
        session.commit()#conectamos la bd
        session.refresh(roomtype)#refrescamos despues de insertar datos
        return roomtype

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
            detail=f"An error occurred while creating romm type: {str(e)}",
        )

    



# obtener room_types por id para eliminar
@router.delete("/api/roomtypes/{roomtype_id}",status_code=status.HTTP_200_OK, tags=["ROOM TYPES"])
def delete_roomtype(roomtype_id: int, session: SessionDep):
    
    try:
        roomtype_db = session.get(RoomType, roomtype_id)
        if not roomtype_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
            )
        session.delete(roomtype_db)
        session.commit()
        return {"detail": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting user type: {str(e)}",
        )

# obtener tipo de habitacion por id para actualizar
@router.patch("/api/roomtypes/{roomtype_id}", response_model=RoomType, tags=["ROOM TYPES"])
def update_roomtype( roomtype_id: int, roomtype_data: RoomTypeUpdate, session: SessionDep):

    try:
            roomtype_db = session.get(RoomType, roomtype_id)
        
            #validate
            if not roomtype_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
                )#status.http y el codigo y detail es para el mensaje que retorna
            roomtype_data_dict=roomtype_data.model_dump(exclude_unset=True)
            #validador
            if "name" in roomtype_data_dict and roomtype_data_dict["name"] != roomtype_db.name:
                existing_usertype = session.exec(select(RoomType).where(RoomType.name == roomtype_data_dict["name"])).first()
                if existing_usertype and existing_usertype.id != roomtype_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
                    )
            usertype_data_dict=roomtype_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
            roomtype_db.sqlmodel_update(usertype_data_dict)
            session.add(roomtype_db)
            session.commit()
            session.refresh(roomtype_db)
            return roomtype_db

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
            detail=f"An error occurred while creating room type: {str(e)}",
        )