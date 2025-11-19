# 🛍️ Puddle - Marketplace Online

Sistema de marketplace desarrollado con Django que permite a los usuarios comprar y vender artículos, gestionar conversaciones y administrar sus publicaciones.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Funcionalidades](#-funcionalidades)
- [API de Rutas](#-api-de-rutas)
- [Modelos de Datos](#-modelos-de-datos)
- [Despliegue](#-despliegue)
- [Seguridad](#-seguridad)
- [Contribuir](#-contribuir)

---

## ✨ Características

- 🔐 **Autenticación completa**: Registro, login, logout y recuperación de contraseña
- 📦 **Gestión de artículos**: Crear, editar, eliminar y buscar productos
- 💬 **Sistema de mensajería**: Conversaciones entre compradores y vendedores
- 🏷️ **Categorización**: Organización de productos por categorías
- 🖼️ **Gestión de imágenes**: Carga con validación y eliminación automática
- 📊 **Dashboard personal**: Panel de control para gestionar publicaciones
- 🔍 **Búsqueda avanzada**: Filtrado por categoría y texto
- 📧 **Notificaciones por email**: Sistema de correo integrado
- 🎨 **Interfaz moderna**: Diseño con Tailwind CSS y Jazzmin Admin
- 📄 **Paginación optimizada**: Navegación eficiente en listados grandes
- ⚡ **Índices de BD**: Consultas optimizadas para máximo rendimiento
- 💰 **Precios precisos**: Validación con Decimal para precisión monetaria
- 🗑️ **Limpieza automática**: Eliminación automática de archivos huérfanos

---

## 🛠️ Tecnologías

- **Backend**: Django 4.2.18
- **Base de Datos**: MySQL
- **Frontend**: HTML, Tailwind CSS 3.8.0
- **Admin Panel**: Django Jazzmin 3.0.1
- **Manejo de Imágenes**: Pillow 11.1.0
- **Variables de Entorno**: python-dotenv
- **HTTP Requests**: requests 2.32.3

---

## 📦 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd puddle
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita el archivo `.env` con tus datos:

```env
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=tu-secret-key-aqui
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Crear base de datos

```sql
CREATE DATABASE puddle_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. (Opcional) Poblar base de datos con datos de prueba

```bash
python manage.py seed
```

Para más información, consulta [SEEDING.md](SEEDING.md)

### 9. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Accede a: `http://localhost:8000`

---

## ⚙️ Configuración

### Generar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Configurar Email (Gmail)

1. Habilita la verificación en dos pasos en tu cuenta de Gmail
2. Genera una contraseña de aplicación: https://myaccount.google.com/apppasswords
3. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

### Configurar Archivos Estáticos

```bash
python manage.py collectstatic
```

---

## 📁 Estructura del Proyecto

```
puddle/
├── core/                   # App principal (home, auth, contacto)
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── views_auth.py
│   ├── forms.py
│   └── urls.py
├── item/                   # Gestión de artículos
│   ├── templates/
│   ├── models.py          # Category, Item
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── conversation/           # Sistema de mensajería
│   ├── templates/
│   ├── models.py          # Conversation, ConversationMessage
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── dashboard/              # Panel de usuario
│   ├── templates/
│   ├── views.py
│   └── urls.py
├── puddle/                 # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                  # Archivos subidos
├── .env                    # Variables de entorno (NO en git)
├── .env.example           # Plantilla de variables
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🎯 Funcionalidades

### Autenticación y Usuarios

- **Registro de usuarios**: Formulario con validación
- **Login/Logout**: Autenticación segura
- **Recuperación de contraseña**: Vía email
- **Perfil de usuario**: Gestión de publicaciones propias

### Gestión de Artículos

- **Crear artículo**: Con imagen, descripción, precio y categoría
- **Editar artículo**: Solo el propietario puede editar
- **Eliminar artículo**: Solo el propietario puede eliminar
- **Marcar como vendido**: Estado de venta
- **Búsqueda**: Por nombre, descripción y categoría
- **Artículos relacionados**: Sugerencias por categoría

### Sistema de Mensajería

- **Iniciar conversación**: Contactar al vendedor
- **Bandeja de entrada**: Ver todas las conversaciones
- **Chat en tiempo real**: Intercambio de mensajes
- **Eliminar mensajes**: Solo mensajes propios
- **Prevención de duplicados**: Una conversación por item

### Dashboard

- **Mis artículos**: Lista de publicaciones propias
- **Estadísticas**: Artículos vendidos/disponibles
- **Acceso rápido**: Editar/eliminar artículos

---

## 🗺️ API de Rutas

### Core (Autenticación y Principal)

| Método | Ruta | Vista | Descripción |
|--------|------|-------|-------------|
| GET | `/` | `index` | Página principal |
| GET/POST | `/signup/` | `signup` | Registro de usuario |
| GET/POST | `/login/` | `LoginView` | Inicio de sesión |
| GET | `/logout/` | `logout_view` | Cerrar sesión |
| GET | `/contact/` | `contact` | Página de contacto |
| POST | `/send_email/` | `enviar_correo` | Enviar email de contacto |
| GET/POST | `/password_reset/` | `CustomPasswordResetView` | Solicitar reset |
| GET | `/password_reset/done/` | `PasswordResetDoneView` | Confirmación enviada |
| GET/POST | `/reset/<uidb64>/<token>/` | `CustomPasswordResetConfirmView` | Confirmar reset |
| GET | `/reset/done/` | `CustomPasswordResetCompleteView` | Reset completado |

### Items (Artículos)

| Método | Ruta | Vista | Descripción | Auth |
|--------|------|-------|-------------|------|
| GET | `/items/` | `items` | Listar artículos | No |
| GET | `/items/<int:pk>/` | `detail` | Detalle de artículo | No |
| GET/POST | `/items/new/` | `new` | Crear artículo | Sí |
| GET/POST | `/items/<int:pk>/edit/` | `edit` | Editar artículo | Sí |
| POST | `/items/<int:pk>/delete/` | `delete` | Eliminar artículo | Sí |

**Parámetros de búsqueda:**
- `?query=texto` - Buscar por nombre/descripción
- `?category=id` - Filtrar por categoría

### Conversations (Mensajería)

| Método | Ruta | Vista | Descripción | Auth |
|--------|------|-------|-------------|------|
| GET | `/inbox/` | `inbox` | Bandeja de entrada | Sí |
| GET/POST | `/inbox/<int:pk>/` | `detail` | Ver conversación | Sí |
| GET/POST | `/inbox/new/<int:item_pk>/` | `new_conversation` | Nueva conversación | Sí |
| POST | `/inbox/eliminar/<int:message_id>/` | `eliminar_mensaje` | Eliminar mensaje | Sí |

### Dashboard

| Método | Ruta | Vista | Descripción | Auth |
|--------|------|-------|-------------|------|
| GET | `/dashboard/` | `index` | Panel de usuario | Sí |

### Admin

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/admin/` | Panel de administración Django |

---

## 💾 Modelos de Datos

### Category (Categoría)

```python
- id: AutoField (PK)
- name: CharField(255)
```

### Item (Artículo)

```python
- id: AutoField (PK)
- category: ForeignKey(Category)
- name: CharField(255)
- description: TextField (opcional)
- price: FloatField
- image: ImageField (opcional)
- is_sold: BooleanField (default=False)
- created_by: ForeignKey(User)
- created_at: DateTimeField (auto)
```

### Conversation (Conversación)

```python
- id: AutoField (PK)
- item: ForeignKey(Item)
- members: ManyToManyField(User)
- created_at: DateTimeField (auto)
- modified_at: DateTimeField (auto)
```

### ConversationMessage (Mensaje)

```python
- id: AutoField (PK)
- conversation: ForeignKey(Conversation)
- content: TextField
- created_by: ForeignKey(User)
- created_at: DateTimeField (auto)
```

---

## 🚀 Despliegue

### PythonAnywhere

1. **Subir código**:
```bash
git clone <tu-repo> /home/tu_usuario/puddle
```

2. **Crear virtualenv**:
```bash
mkvirtualenv --python=/usr/bin/python3.10 puddle-env
pip install -r requirements.txt
```

3. **Configurar Web App**:
   - Source code: `/home/tu_usuario/puddle`
   - Working directory: `/home/tu_usuario/puddle`
   - WSGI file: Configurar ruta a `puddle/wsgi.py`

4. **Variables de entorno**:
   - Agregar en el archivo WSGI o usar .env

5. **Archivos estáticos**:
```bash
python manage.py collectstatic
```

6. **Base de datos**:
   - Crear MySQL database en PythonAnywhere
   - Configurar credenciales en `.env`
   - Ejecutar migraciones

### Heroku

```bash
# Instalar Heroku CLI y login
heroku login

# Crear app
heroku create tu-app-name

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variables
heroku config:set SECRET_KEY="tu-secret-key"
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Migraciones
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 🔒 Seguridad

### Buenas Prácticas Implementadas

✅ **Variables de entorno**: Credenciales fuera del código
✅ **SECRET_KEY segura**: Generada aleatoriamente
✅ **DEBUG=False en producción**: Evita exposición de información
✅ **ALLOWED_HOSTS configurado**: Previene ataques de host header
✅ **CSRF Protection**: Habilitado por defecto
✅ **Password Validators**: Validación robusta de contraseñas
✅ **SQL Injection Protection**: ORM de Django
✅ **XSS Protection**: Templates auto-escapan HTML
✅ **.gitignore**: Archivos sensibles excluidos

### Recomendaciones Adicionales

- 🔐 Usar HTTPS en producción
- 🔑 Rotar SECRET_KEY periódicamente
- 📧 Usar contraseñas de aplicación para email
- 🗄️ Backups regulares de la base de datos
- 📊 Monitorear logs de acceso
- 🚫 Limitar intentos de login
- 🔄 Mantener dependencias actualizadas

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Test de una app específica
python manage.py test item

# Con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📝 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar base de datos con datos de prueba
python manage.py seed

# Limpiar y poblar base de datos
python manage.py seed --clear

# Limpiar imágenes huérfanas (ver qué se eliminaría)
python manage.py cleanup_images --dry-run

# Limpiar imágenes huérfanas (eliminar)
python manage.py cleanup_images

# Shell interactivo
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar problemas
python manage.py check

# Limpiar sesiones expiradas
python manage.py clearsessions
```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👤 Autor

**Joel Rojas**
- Email: rojassebas765@gmail.com

---

## 🙏 Agradecimientos

- Django Framework
- Tailwind CSS
- Django Jazzmin
- Comunidad de Python

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

---

**⚠️ Nota de Seguridad**: Nunca compartas tu archivo `.env` o credenciales en repositorios públicos. Consulta `SECURITY_ALERT.md` para más información sobre seguridad.
