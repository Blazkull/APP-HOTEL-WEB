from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select, Session

from models.room_status import RoomStatus, RoomStatusCreate, RoomStatusUpdate
from core.database import SessionDep

router = APIRouter()


# lista de tipos de habitacion
@router.get("/api/roomstatus", response_model=list[RoomStatus], tags=["ROOM STATUS"])
def list_roomstatus(session: SessionDep):
    try:
        return session.exec(select(RoomStatus)).all()  # esto ejecuta transacciones de sql
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while listing room statuses: {str(e)}",
        )


# obtener tipo de habitacion por id para listar
@router.get("/api/roomstatus/{roomstatus_id}", response_model=RoomStatus, tags=["ROOM STATUS"])
def read_roomstatus(roomstatus_id: int, session: SessionDep):
    try:
        roomstatus_db = session.get(RoomStatus, roomstatus_id)
        if not roomstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room status not found"
            )  # status.http y el codigo y detail es para el mensaje que retorna
        return roomstatus_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while reading room status: {str(e)}",
        )



# crear tipo de habitacion
@router.post("/api/roomstatus", response_model=RoomStatus, status_code=status.HTTP_201_CREATED, tags=["ROOM STATUS"])
def create_roomstatus(room_status_data: RoomStatusCreate, session: SessionDep):
    try:
        # roomstatus = RoomStatus.model_validate(room_status_data.model_dump())  # No es necesario con SQLModel
        roomstatus = RoomStatus(name=room_status_data.name, description=room_status_data.description) #forma correcta de crear la instancia con SQLModel
        existing_roomstatus = session.exec(select(RoomStatus).where(RoomStatus.name == roomstatus.name)).first()
        if existing_roomstatus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Room status name already exists"
            )
        session.add(roomstatus)  # insertamos datos
        session.commit()  # conectamos la bd
        session.refresh(roomstatus)  # refrescamos despues de insertar datos
        return roomstatus
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,  # Use 422 for validation errors
            detail=f"Invalid input data: {str(ve)}",
        )
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while creating room status: {str(e)}",
        )



# obtener room_status por id para eliminar
@router.delete("/api/roomstatus/{roomstatus_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["ROOM STATUS"])
def delete_roomstatus(roomstatus_id: int, session: SessionDep):
    try:
        roomstatus_db = session.get(RoomStatus, roomstatus_id)
        if not roomstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room status not found"
            )
        session.delete(roomstatus_db)
        session.commit()
        return {"detail": "Room status deleted successfully"}  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting room status: {str(e)}",
        )



# obtener tipo de habitacion por id para actualizar
@router.patch("/api/roomstatus/{roomstatus_id}", response_model=RoomStatus, tags=["ROOM STATUS"])
def update_roomstatus(roomstatus_id: int, roomstatus_data: RoomStatusUpdate, session: SessionDep):
    try:
        roomstatus_db = session.get(RoomStatus, roomstatus_id)
        if not roomstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room status not found"
            )  # status.http y el codigo y detail es para el mensaje que retorna

        roomstatus_data_dict = roomstatus_data.model_dump(exclude_unset=True)  # esto evita que se envien datos vacios a la base de datos
        if "name" in roomstatus_data_dict and roomstatus_data_dict["name"] != roomstatus_db.name:
            existing_roomstatus = session.exec(select(RoomStatus).where(RoomStatus.name == roomstatus_data_dict["name"])).first()
            if existing_roomstatus and existing_roomstatus.id != roomstatus_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Room status name already exists"
                )
        roomstatus_db.sqlmodel_update(roomstatus_data_dict)
        session.add(roomstatus_db)
        session.commit()
        session.refresh(roomstatus_db)
        return roomstatus_db
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input data: {str(ve)}",
        )
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating room status: {str(e)}",
        )
