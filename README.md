recycling-management-api

Proyecto #2 Desarrollo de Software III — Universidad de Costa Rica
Sistema de Gestión de Reciclaje Comunitario — API REST

Descripción

Aplicación web desarrollada en Python para gestionar procesos de reciclaje comunitario. El sistema permite administrar recicladores, puntos de recolección, entregas de materiales y generar reportes a partir de la información almacenada.

El proyecto utiliza una arquitectura cliente-servidor, donde el backend expone una API REST con FastAPI y el frontend consume los servicios mediante JavaScript.

---

Tecnologías

| Capa                 | Tecnología            |
| -------------------- | --------------------- |
| Backend              | Python + FastAPI      |
| ORM                  | SQLAlchemy            |
| Base de datos        | MySQL                 |
| Validación           | Pydantic              |
| Servidor             | Uvicorn               |
| Frontend             | HTML, CSS, JavaScript |
| Control de versiones | Git/GitHub            |

---

Arquitectura

El proyecto está organizado por capas:

```
Router
   ↓
Service
   ↓
Repository
   ↓
Model
   ↓
Base de datos
```

Router:** maneja las peticiones HTTP.
Service:** contiene las reglas del sistema.
Repository:** gestiona el acceso a datos.
Model:** representa las tablas de la base de datos.

---

Funcionalidades principales

Autenticación

Permite iniciar sesión y proteger rutas mediante token.

Recicladores

* Registrar usuarios.
* Consultar, actualizar y desactivar recicladores.
* Filtrar información.

Puntos de recolección

* Crear y administrar centros.
* Definir materiales aceptados.
* Controlar capacidad disponible.

Entregas

* Registrar materiales entregados.
* Validar usuarios, materiales y capacidad del punto.
* Actualizar cantidades automáticamente.

Reportes

* Ranking de recicladores.
* Estado de puntos de recolección.
* Cantidad recolectada por material.
* Filtros por fecha.

---

Estructura del proyecto

```
app/
├── models/          # Modelos de base de datos
├── schemas/         # Validaciones
├── repositories/    # Acceso a datos
├── services/        # Lógica de negocio
└── routers/         # Endpoints API

templates/           # Frontend HTML
static/              # CSS y JavaScript
main.py              # Inicio de la aplicación
```

---

Instalación

Clonar repositorio:

```bash
git clone https://github.com/fhernandezz/recycling-management-api.git
cd recycling-management-api
```

Activar entorno virtual:

```bash
.venv\Scripts\activate
```

Configurar la base de datos en:

```
config/database.py
```

Ejecutar:

```bash
uvicorn main:app --reload
```

---

Rutas principales

| Ruta        | Función               |
| ----------- | --------------------- |
| `/`         | Login                 |
| `/usuarios` | Recicladores          |
| `/centros`  | Puntos de recolección |
| `/entregas` | Registro de entregas  |
| `/reportes` | Estadísticas          |
| `/docs`     | Swagger API           |

---

Integrantes

* Fabricio Hernández López
* Brayan Salamanca
* Valentina Badilla Morera
