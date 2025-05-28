# 🏨 Aplicación Web de Gestión de Reservas Hoteleras

¡Bienvenido al proyecto de gestión de reservas hoteleras! Este repositorio contiene tanto el **backend (API RESTful)** como el **frontend (Interfaz de Usuario Web)** de la aplicación, diseñados para trabajar en conjunto y ofrecer una solución completa para la administración de habitaciones, clientes, reservas y más.

---

## 🌟 Visión General del Proyecto

Este sistema integral permite la gestión eficiente de un hotel, desde el registro de habitaciones y clientes hasta la creación y control de reservas. El **backend**, desarrollado con FastAPI, actúa como el cerebro de la aplicación, proporcionando una API robusta y escalable. El **frontend**, construido con tecnologías web estándar (HTML, CSS, JavaScript), ofrece una interfaz de usuario intuitiva para interactuar con todas las funcionalidades del sistema.

### Funciones Clave:

* **Gestión de Habitaciones:** Administración de habitaciones y sus diferentes tipos (individual, doble, suite, etc.).
* **Gestión de Clientes:** Registro y administración de la información de los clientes.
* **Gestión de Reservas:** Creación, consulta, modificación y cancelación de reservas, con control de estados (pendiente, confirmada, cancelada).
* **Administración de Usuarios:** Control de usuarios y roles dentro del sistema.
* **Panel de Control (Dashboard):** Vista general con información relevante (disponible en el frontend).

---

## 🚀 Tecnologías Utilizadas

### Backend

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-blue.svg)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-DataValidation-lightgrey.svg)](https://pydantic-docs.helpmanual.io/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-blueviolet.svg)](https://www.uvicorn.org/)

* **Python 3.10+**: Lenguaje de programación principal.
* **FastAPI**: Framework web de alto rendimiento para construir la API RESTful.
* **MySQL 8+**: Sistema de gestión de bases de datos relacionales.
* **SQLAlchemy**: ORM (Object-Relational Mapper) para interactuar con la base de datos.
* **Pydantic**: Para la validación de datos y la gestión de configuraciones.
* **Python-dotenv**: Para la gestión de variables de entorno.
* **PyMySQL**: Conector Python para MySQL.
* **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.
* **Swagger UI / ReDoc**: Documentación interactiva automática de la API.

### Frontend

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E.svg)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![CSS](https://img.shields.io/badge/CSS-Styling-1572B6.svg)](https://developer.mozilla.org/es/docs/Web/CSS)
[![HTML](https://img.shields.io/badge/HTML5-Markup-E34F26.svg)](https://developer.mozilla.org/es/docs/Web/HTML)
[![Axios](https://img.shields.io/badge/Axios-HTTP%20Client-5A29E4.svg)](https://axios-http.com/es/)

* **HTML**: Para la estructura de las páginas web.
* **CSS**: Para el diseño y estilo visual de la interfaz.
* **JavaScript**: Para la lógica interactiva del lado del cliente.
* **Axios**: Cliente HTTP basado en promesas para realizar peticiones al backend.

### Herramientas de Desarrollo Comunes

[![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-IDE-blue.svg)](https://code.visualstudio.com/)
[![Git](https://img.shields.io/badge/Git-VCS-F05032.svg)](https://git-scm.com/)
[![Warp](https://img.shields.io/badge/Warp-Terminal-black.svg)](https://www.warp.dev/)
[![MySQL Workbench](https://img.shields.io/badge/MySQL%20Workbench-Tool-orange.svg)](https://dev.mysql.com/downloads/workbench/)

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

1.  **Python 3.10 o superior**: [Descargar Python](https://www.python.org/downloads/)
2.  **MySQL Server 8 o superior**: [Descargar MySQL Server](https://dev.mysql.com/downloads/mysql/)
3.  **MySQL Workbench**: [Descargar MySQL Workbench](https://dev.mysql.com/downloads/workbench/) (Para ejecutar scripts SQL y gestionar la DB).
4.  **Git**: [Descargar Git](https://git-scm.com/) (Para clonar el repositorio).
5.  **Un navegador web moderno** (Chrome, Firefox, Edge, etc.).

---

## 🛠️ Configuración y Ejecución del Proyecto (Paso a Paso)

Sigue estos pasos para poner en marcha tanto el backend como el frontend de la aplicación.

### Paso 1: Clonar el Repositorio

Abre tu terminal y ejecuta:

```bash
git clone [https://github.com/Blazkull/APP-RESERVATION-HOTEL-WEB.git](https://github.com/Blazkull/APP-RESERVATION-HOTEL-WEB.git)
cd APP-RESERVATION-HOTEL-WEB
