from typing import List
from fastapi import APIRouter, Query, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select

from models.room import Room, RoomCreate, RoomStatusUpdate, RoomUpdate
from core.database import SessionDep
from models.room_status import RoomStatus

router = APIRouter()


#lista de tipos de room
@router.get("/api/room", response_model=List[Room], tags=["ROOM"])
def list_room(
    session: SessionDep,
    #paginacion
    page: int = Query(1, ge=1, description="Número de página a obtener"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad de items por página"),
    ):
    try:
        offset = (page - 1) * limit
        rooms = session.exec(select(Room).offset(offset).limit(limit)).all()
        return rooms
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting room: {str(e)}",
        )


# obtener tipo de room por id para listar
@router.get("/api/room/{room_id}", response_model=Room, tags=["ROOM"])
def read_room(room_id: int, session: SessionDep):

    try:
        room_db = session.get(Room, room_id)
        if not room_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exits"
            )#status.http y el codigo y detail es para el mensaje que retorna
        return room_db
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
            detail=f"An error occurred while creating room: {str(e)}",
        )
#crear tipo de room
@router.post("/api/room", response_model=Room, status_code=status.HTTP_201_CREATED ,tags=["ROOM"])
def create_room(room_data: RoomCreate,session: SessionDep):

    try:
        room = Room.model_validate(room_data.model_dump())
        existing_room=session.exec(select(Room).where(Room.room_number == room.room_number)).first()
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="Room already registered"
            )
        session.add(room)#insertamos datos
        session.commit()#conectamos la bd
        session.refresh(room)#refrescamos despues de insertar datos
        return room
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
            detail=f"An error occurred while creating room: {str(e)}",
        )



#actualizar estado de habitacion
@router.patch("/api/room/{room_id}/status", response_model=dict, status_code=status.HTTP_200_OK, tags=["ROOM"])
def update_room_status(room_id: int, status_update: RoomStatusUpdate, session: SessionDep):
    try:
        room_db = session.get(Room, room_id)
        if not room_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exist"
            )

        # Evita actualizar si el estado no ha cambiado
        if status_update.active == room_db.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="New status is the same as the current one"
            )

        room_db.active = status_update.active       
        session.add(room_db)
        session.commit()
        session.refresh(room_db)

        return {"message": f"Room: '{room_db.room_number}' has successfully updated their status to: {room_db.active}"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating status: {str(e)}",
        )


# obtener tipo de room por id para actualizar
@router.patch("/api/room/{room_id}", response_model=Room, status_code=status.HTTP_200_OK, tags=["ROOM"])
def update_room( room_id: int, room_data: RoomUpdate, session: SessionDep):

    try:
        room_db = session.get(Room, room_id)
        if not room_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exits"
            )#status.http y el codigo y detail es para el mensaje que retorna
        room_data_dict=room_data.model_dump(exclude_unset=True)
        if "room_number" in room_data_dict and room_data_dict["room_number"] != room_db.room_number:
                existing_room = session.exec(select(Room).where(Room.room_number == room_data_dict["room_number"])).first()
                if existing_room and existing_room.id != room_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Room already registered"
                    )
        room_db.sqlmodel_update(room_data_dict)
        session.add(room_db)
        session.commit()
        session.refresh(room_db)
        return room_db
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
            detail=f"An error occurred while creating room: {str(e)}",
        )