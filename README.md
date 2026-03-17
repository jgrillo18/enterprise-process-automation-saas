# Enterprise Process Automation SaaS

![Stack](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square&logo=flask)
![Stack](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql)
![Stack](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens)
![Deploy](https://img.shields.io/badge/Live-Render-46E3B7?style=flat-square&logo=render)

Mini plataforma SaaS para automatización de procesos internos empresariales.

Diseñada para digitalizar flujos manuales como:
- Gestión de tickets
- Solicitudes internas
- Tareas operativas
- Aprobaciones
- Procesos basados en Excel, correos o WhatsApp

---

## 🚀 Live Demo

| Servicio | URL |
|----------|-----|
| **Aplicación** | https://enterprise-process-automation.onrender.com |

> **Credenciales de demo**
> - Usuario: `admin`
> - Contraseña: `admin`
>
> **Nota:** La instancia gratuita de Render puede tardar ~30 segundos en despertar tras inactividad.

---

## 🚀 Características principales

- Autenticación segura con JWT
- Sistema de roles (admin / user)
- Creación y gestión de procesos
- Historial de auditoría
- Logging estructurado
- Arquitectura modular escalable
- Docker ready
- PostgreSQL

> **Credencial de demostración**
> Al arrancar el contenedor por primera vez el sistema crea automáticamente un usuario con rol **admin**.
> - Usuario: `admin`
> - Contraseña: `admin`
> 
> Usa esta cuenta para acceder al dashboard y crear más usuarios. No olvides cambiarla o eliminarla en producción.

---

## 🧠 Arquitectura

Backend basado en Flask con arquitectura modular:

- Models → Entidades del sistema
- Services → Lógica de negocio
- Routes → Endpoints REST
- Utils → Seguridad y logging
- Extensions → Inicialización centralizada

Base de datos: PostgreSQL  
Servidor: Gunicorn  
Contenedorización: Docker  

---

## 📦 Estructura del Proyecto
enterprise-process-automation-saas/
│
├── app/
│ ├── models/
│ ├── routes/
│ ├── services/
│ ├── utils/
│ └── extensions.py
| └──templates/
│ |  ├── base.html
│ |  ├── login.html
│ |  ├── dashboard.html
│ └──static/
│    ├── css/style.css
│    └── js/app.js
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py


---

## ⚙️ Instalación con Docker

Antes de levantar los contenedores, revisa o crea el archivo `.env` en la raíz del proyecto. Para facilitar, hay un `.env.example` con valores ficticios que puedes copiar y ajustar:

```
cp .env.example .env
# edita .env con tus claves
```

Ejemplo mínimo de contenido:

```
FLASK_ENV=development
SECRET_KEY=una_clave_larga_y_segura
DATABASE_URL=postgresql://postgres:postgres@db:5432/enterprise
JWT_SECRET_KEY=otra_clave_larga
```

Puedes cambiar las credenciales de la base de datos, el puerto y otras variables según sea necesario.

```bash
docker-compose up --build
```

## La aplicación quedará disponible en:
http://localhost:5000

**Nota:** si haces `docker-compose down` y borras el volumen `postgres_data`, se regenerará el usuario `admin` con contraseña `admin` al iniciar de nuevo.

---

### 📢 Despliegue en GitHub Pages

Para publicar una demo estática en GitHub Pages se utiliza un flujo de GitHub Actions.
El contenido que se entrega es el que pongas en la carpeta `docs/`.

1. Crea un **Personal Access Token (PAT)** en tu cuenta de GitHub con el alcance `repo`.
   - Entra a https://github.com/settings/tokens → Generate new token → selecciona `repo` scope → crear.
2. Añade el token como secreto en tu repositorio: Settings → Secrets → Actions → New repository secret.
   - Nombre sugerido: `GH_PAT`.
3. Cada vez que hagas `git push` a `main`, el workflow (`.github/workflows/pages.yml`) tomará ese token y subirá los archivos de `docs/` a la rama `gh-pages`.
4. Activa GitHub Pages en Settings → Pages seleccionando “GitHub Actions” como fuente.

La URL resultante será:
`https://jgrillo18.github.io/enterprise-process-automation-saas-/` (ajusta si cambias el nombre del repo).

Podrás actualizar la demo simplemente modificando la carpeta `docs/` y haciendo push.

## 🔐 Endpoints principales

> **Credenciales iniciales**
> - Usuario: `admin`
> - Contraseña: `admin`
> - Rol: `admin` (se crea automáticamente al levantar la aplicación)

Registro

  - POST /api/auth/register  (admin puede crear usuarios)
- Login
  - POST /api/auth/login
- Crear proceso
  - POST /api/process/
- Listar procesos
  - GET /api/process/
- Admin UI:
  - Listar usuarios  GET /api/auth/users
  - Ver logs (solo admin) GET /api/admin/logs

La interfaz web ofrece:
- Dashboard con tarjetas para procesos, estadísticas rápidas (conteo) y, si eres admin, secciones para usuarios y logs
- Banner de bienvenida con nombre y rol
- Formularios interactivos con validación
- Navegación simple, adaptada para subir a GitHub como demostración

## FRONTEND MINIMALISTA

Frontend  usando:

- Jinja templates
- Fetch API
- CSS moderno
- Sin frameworks pesados
- Estética SaaS minimalista

---

## 🛡 Seguridad

- Password hashing con Werkzeug
- JWT para autenticación stateless
- Control de roles
- Logs de auditoría
- Separación por capas

## 📈 Casos de uso empresariales

- Digitalización de procesos internos
- Gestión de solicitudes
- Automatización operativa
- Control de trazabilidad
- Base para motor BPM

## 🛣 Roadmap

- Multi-tenant
- Webhooks
- Integraciones API externas
- Panel UI avanzado
- Notificaciones reales (email / Slack)
- Workflow dinámico configurable

## 👨‍💻 Autor

Jhonnathan Grillo
Ingeniero de Sistemas
Automatización Empresarial | Arquitectura SaaS | Analítica de Datos