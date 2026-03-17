# Enterprise Process Automation SaaS

![Stack](https://img.shields.io/badge/Backend-Flask_3.0-000000?style=flat-square&logo=flask)
![Stack](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql)
![Stack](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens)
![Stack](https://img.shields.io/badge/Frontend-Bootstrap_5-7952B3?style=flat-square&logo=bootstrap)
![Stack](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render)
![Stack](https://img.shields.io/badge/Container-Docker-2496ED?style=flat-square&logo=docker)
![Stack](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=flat-square)

Plataforma SaaS modular para automatización de procesos internos empresariales, construida con Flask, JWT, roles, PostgreSQL y Docker. Incluye interfaz web responsiva con soporte PWA e internacionalización ES/EN.

---

## 🌐 Demo en vivo

| Servicio | URL |
|---|---|
| **Aplicación** | **https://enterprise-process-automation.onrender.com** |

### Credenciales de demo

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `admin` |
| Correo de contacto | jhonnathan@jgrillo.tech |

> ⚠️ La instancia gratuita de Render puede tardar ~30 segundos en despertar tras inactividad.

---

## ✨ Características principales

| Categoría | Detalle |
|---|---|
| **Autenticación** | JWT stateless, login/logout, tokens seguros |
| **Roles** | `admin` y `user` con vistas diferenciadas |
| **Procesos** | Crear, listar y gestionar con estados y descripción |
| **Datos demo** | Botón "⚡ Cargar datos demo" — genera 8 procesos empresariales realistas |
| **Auditoría** | Log de acciones con timestamps |
| **Usuarios** | El admin puede crear y listar usuarios desde el dashboard |
| **PWA** | Instalable en Android, Windows y macOS como app nativa |
| **i18n** | Cambio de idioma ES/EN desde la navbar (persiste en localStorage) |
| **Docker** | Imagen lista para producción con Gunicorn |
| **Estáticos** | Servidos con WhiteNoise (MIME types correctos en producción) |

---

## 🖥️ Interfaz

- **Login**: Banner de presentación freelancer con credenciales, servicios ofrecidos y formulario al lado.
- **Dashboard**: Panel con estadísticas, creación de procesos, lista con estados coloreados, gestión de usuarios (admin) y logs de auditoría.
- **Navbar**: Muestra usuario autenticado, botón de idioma y "Cerrar sesión" (solo visible cuando hay sesión activa).

---

## 🧠 Arquitectura

```
enterprise-process-automation-saas/
│
├── app/
│   ├── __init__.py           # App factory (Flask, WhiteNoise, rutas, DB init)
│   ├── config.py             # Config con fallback SQLite + fix postgres://
│   ├── extensions.py         # db, jwt, migrate
│   ├── models/
│   │   └── user.py           # Modelo User con hash de contraseña
│   ├── routes/
│   │   ├── auth_routes.py    # /api/auth/login, /register, /users
│   │   ├── process_routes.py # /api/process/ CRUD + /demo
│   │   └── admin_routes.py   # /api/admin/logs
│   ├── services/
│   ├── utils/
│   │   └── logger.py
│   ├── templates/
│   │   ├── base.html         # Layout: Bootstrap 5, i18n, PWA, navbar
│   │   ├── login.html        # Banner demo + formulario
│   │   └── dashboard.html    # Panel principal
│   └── static/
│       ├── css/style.css
│       ├── js/app.js
│       ├── manifest.json     # PWA manifest
│       ├── sw.js             # Service Worker (cache network-first)
│       └── img/icon.svg      # Icono PWA
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml               # Configuracion de despliegue en Render
├── requirements.txt
└── run.py
```

---

## 🔌 Endpoints REST

### Autenticación

| Método | Ruta | Descripción | Auth requerida |
|---|---|---|---|
| `POST` | `/api/auth/login` | Obtener token JWT | No |
| `POST` | `/api/auth/register` | Crear usuario | ✅ admin |
| `GET` | `/api/auth/users` | Listar usuarios | ✅ admin |

### Procesos

| Método | Ruta | Descripción | Auth requerida |
|---|---|---|---|
| `POST` | `/api/process/` | Crear proceso | ✅ |
| `GET` | `/api/process/` | Listar procesos | ✅ |
| `POST` | `/api/process/demo` | Cargar 8 procesos de ejemplo | ✅ |

### Admin

| Método | Ruta | Descripción | Auth requerida |
|---|---|---|---|
| `GET` | `/api/admin/logs` | Ver log de auditoría | ✅ admin |

---

## 📦 Instalación local con Docker

```bash
# 1. Clonar el repositorio
git clone https://github.com/jgrillo18/enterprise-process-automation-saas.git
cd enterprise-process-automation-saas

# 2. Crear .env (copia el ejemplo y ajusta)
cp .env.example .env

# 3. Levantar contenedores
docker-compose up --build
```

La aplicación quedará disponible en **http://localhost:5000**

### Variables de entorno requeridas (`.env`)

```env
FLASK_ENV=development
SECRET_KEY=una_clave_larga_y_segura
DATABASE_URL=postgresql://postgres:postgres@db:5432/enterprise
JWT_SECRET_KEY=otra_clave_secreta
```

> El usuario `admin` / `admin` se crea automáticamente al iniciar si no existe.

---

## 🚀 Despliegue en Render

El archivo `render.yaml` incluido configura el servicio automáticamente:

```yaml
services:
  - type: web
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app --bind 0.0.0.0:$PORT --workers 2
```

Pasos:
1. Conecta el repositorio en [render.com](https://render.com)
2. Añade `DATABASE_URL` apuntando a tu PostgreSQL (ej. Neon.tech)
3. Añade `SECRET_KEY` y `JWT_SECRET_KEY`
4. Render despliega automáticamente en cada push a `main`

---

## 🛡️ Seguridad

- Contraseñas hasheadas con **Werkzeug** (PBKDF2-SHA256)
- Autenticación stateless con **JWT** (`flask-jwt-extended`)
- Control de acceso por rol en cada endpoint
- Logs de auditoría para acciones críticas
- Variables sensibles en variables de entorno (nunca en código)
- `postgres://` corregido a `postgresql://` para compatibilidad con SQLAlchemy 2.x

---

## 📈 Casos de uso

- Digitalización de procesos internos manuales
- Gestión de solicitudes y aprobaciones
- Automatización operativa
- Control de trazabilidad empresarial
- Base extensible para un motor BPM completo

---

## 🛣️ Roadmap

- [ ] Multi-tenant
- [ ] Webhooks
- [ ] Integraciones con APIs externas
- [ ] Notificaciones reales (email / Slack)
- [ ] Workflow dinámico configurable
- [ ] Panel de analítica avanzado

---

## 👨‍💻 Autor

**Jhonnathan Grillo**
Ingeniero de Sistemas · Automatización Empresarial · Arquitectura SaaS · Analítica de Datos
✉️ jhonnathan@jgrillo.tech
