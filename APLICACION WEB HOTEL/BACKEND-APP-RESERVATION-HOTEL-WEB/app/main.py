import os
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi import FastAPI, Request
from core.database import create_db_and_tables
from routers import login, usertypes, users, clients, roomtypes, roomstatus, room, reservations, reservation_statues,dashboard
from fastapi.middleware.cors import CORSMiddleware  # habilitar CORS

from fastapi.staticfiles import StaticFiles


app = FastAPI()


# montar carpeta 'static' para servir archivos como PDFs, imágenes, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "API en línea en Render"}



# Inclusión de rutas
app.include_router(usertypes.router)
app.include_router(users.router)
app.include_router(login.router) 
app.include_router(roomtypes.router)
app.include_router(roomstatus.router)
app.include_router(room.router)
app.include_router(clients.router)
app.include_router(reservation_statues.router)
app.include_router(reservations.router)
app.include_router(dashboard.router)





# Configuración de CORS
origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "https://mi-dominio.com",
    "https://otro-dominio.net",
    
    "*",  # Solo para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#parametro para conectar con render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)