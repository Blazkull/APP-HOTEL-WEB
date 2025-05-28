from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select

from models.reservation_status import ReservationStatus, ReservationStatusCreate, ReservationStatusUpdate
from core.database import SessionDep

router = APIRouter()


# lista de estados de reserva
@router.get("/api/reservationstatus", response_model=list[ReservationStatus], tags=["RESERVATION STATUS"])
def list_reservation_status(session: SessionDep):
    try:
        return session.exec(select(ReservationStatus)).all()# esto ejecuta transacciones de sql
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while listing room statuses: {str(e)}",
        )

# obtener estado de reserva por id para listar
@router.get("/api/reservationstatus/{reservationstatus_id}", response_model=ReservationStatus, tags=["RESERVATION STATUS"])
def read_reservation_status(reservationstatus_id: int, session: SessionDep):
    try:
    
        reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
        if not reservationstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
            )# status.http y el codigo y detail es para el mensaje que retorna
        return reservationstatus_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while reading room status: {str(e)}",
        )

# crear estado de reserva
@router.post("/api/reservationstatus", response_model=ReservationStatus, status_code=status.HTTP_201_CREATED, tags=["RESERVATION STATUS"])
def create_reservation_status(reservation_status_data: ReservationStatusCreate, session: SessionDep):
   

    
    try:
            reservation_status = ReservationStatus.model_validate(reservation_status_data.model_dump())
            existing_reservationstatus = session.exec(select(ReservationStatus).where(ReservationStatus.name == reservation_status.name)).first()
            if existing_reservationstatus:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Room status name already exists"
                )
            session.add(reservation_status)# insertamos datos
            session.commit()# conectamos la bd
            session.refresh(reservation_status)# refrescamos despues de insertar datos
            return reservation_status
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
            detail=f"An unexpected error occurred while creating reservation status: {str(e)}",
        )



# obtener reservation_status por id para eliminar
@router.delete("/api/reservationstatus/{reservationstatus_id}", status_code=status.HTTP_200_OK, tags=["RESERVATION STATUS"])
def delete_reservation_status(reservationstatus_id: int, session: SessionDep):
    try:
        reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
        if not reservationstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
            )
        session.delete(reservationstatus_db)
        session.commit()
        return {"detail": "Reservation Status deleted succesfully"}
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting room status: {str(e)}",
            )
# obtener estado de reserva por id para actualizar
@router.patch("/api/reservationstatus/{reservationstatus_id}", response_model=ReservationStatus, tags=["RESERVATION STATUS"])
def update_reservation_status( reservationstatus_id: int, reservation_status_data: ReservationStatusUpdate, session: SessionDep):
    
    try:
    
        reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
        if not reservationstatus_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
            )# status.http y el codigo y detail es para el mensaje que retorna
        reservation_status_data_dict = reservation_status_data.model_dump(exclude_unset=True)
        if "name" in reservation_status_data_dict and reservation_status_data_dict["name"] != reservationstatus_db.name:
            existing_roomstatus = session.exec(select(ReservationStatus).where(ReservationStatus.name == reservation_status_data_dict["name"])).first()
            if existing_roomstatus and existing_roomstatus.id != reservationstatus_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Room status name already exists"
                )

       
        reservationstatus_db.sqlmodel_update(reservation_status_data_dict)
        session.add(reservationstatus_db)
        session.commit()
        session.refresh(reservationstatus_db)
        return reservationstatus_db
    
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
            detail=f"An unexpected error occurred while updating reservation status: {str(e)}",
        )