from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select, desc # Import 'desc'
from models.client import Client, ClientCreate, ClientStatus, ClientUpdate
from core.database import SessionDep

router = APIRouter()

# lista de tipos de usuario
@router.get("/api/client", response_model=list[Client], tags=["CLIENT"])
def list_client(session: SessionDep):
    try:
        # Sort by ID in descending order
        clients = session.exec(select(Client).order_by(desc(Client.id))).all()
        return clients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving clients: {str(e)}",
        )

# obtener tipo de usuario por id para listar
@router.get("/api/client/{client_id}", response_model=Client, tags=["CLIENT"])
def read_client(client_id: int, session: SessionDep):
    try:
        client_db = session.get(Client, client_id)
        if not client_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exist"
            )
        return client_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving client: {str(e)}",
        )


# crear tipo de usuario
@router.post("/api/client", response_model=Client, status_code=status.HTTP_201_CREATED, tags=["CLIENT"])
def create_client(client_data: ClientCreate, session: SessionDep):
    
    try:
        # Validate data base
        client = Client.model_validate(client_data.model_dump())

        # Check for uniqueness of phone, email, and number_identification
        existing_phone = session.exec(select(Client).where(Client.phone == client.phone)).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered"
            )

        existing_email = session.exec(select(Client).where(Client.email == client.email)).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )

        existing_identification = session.exec(
            select(Client).where(Client.number_identification == client.number_identification)
        ).first()
        if existing_identification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Number identification already registered"
            )

        session.add(client)
        session.commit()
        session.refresh(client)
        return client
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
            detail=f"An error occurred while creating client: {str(e)}",
        )



#actualizar estado de usuario
@router.patch("/api/client/{client_id}/status", response_model=dict, status_code=status.HTTP_200_OK, tags=["CLIENT"])
def update_client_status(client_id: int, status_update: ClientStatus, session: SessionDep):
    try:
        client_db = session.get(Client, client_id)
        if not client_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exist"
            )

        # Evita actualizar si el estado no ha cambiado
        if status_update.active == client_db.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="New status is the same as the current one"
            )

        client_db.active = status_update.active       
        session.add(client_db)
        session.commit()
        session.refresh(client_db)

        return {"message": f"Client '{client_db.first_name} {client_db.last_name}' has successfully updated their status to: {client_db.active}"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating status: {str(e)}",
        )
    

# obtener tipo de usuario por id para actualizar
@router.patch("/api/client/{client_id}", response_model=Client, status_code=status.HTTP_200_OK, tags=["CLIENT"])
def update_client(client_id: int, client_data: ClientUpdate, session: SessionDep):

    try:
        client_db = session.get(Client, client_id)
        if not client_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exist"
            )

        client_data_dict = client_data.model_dump(exclude_unset=True)  # Avoid sending empty data

        # Check for uniqueness before updating
        if "phone" in client_data_dict and client_data_dict["phone"] != client_db.phone:
            existing_phone = session.exec(select(Client).where(Client.phone == client_data_dict["phone"])).first()
            if existing_phone and existing_phone.id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered"
                )

        if "email" in client_data_dict and client_data_dict["email"] != client_db.email:
            existing_email = session.exec(select(Client).where(Client.email == client_data_dict["email"])).first()
            if existing_email and existing_email.id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
                )

        if "number_identification" in client_data_dict and client_data_dict["number_identification"] != client_db.number_identification:
            existing_identification = session.exec(
                select(Client).where(Client.number_identification == client_data_dict["number_identification"])
            ).first()
            if existing_identification and existing_identification.id != client_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Number identification already registered"
                )

        client_db.sqlmodel_update(client_data_dict)
        session.add(client_db)
        session.commit()
        session.refresh(client_db)
        return client_db
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating client: {str(e)}",
        )