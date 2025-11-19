# 📚 Documentación Técnica - Puddle Marketplace

## Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Modelos de Datos](#modelos-de-datos)
3. [Vistas y Lógica de Negocio](#vistas-y-lógica-de-negocio)
4. [Formularios](#formularios)
5. [Sistema de Autenticación](#sistema-de-autenticación)
6. [Sistema de Mensajería](#sistema-de-mensajería)
7. [Gestión de Archivos](#gestión-de-archivos)
8. [Configuración](#configuración)
9. [Base de Datos](#base-de-datos)
10. [API Endpoints](#api-endpoints)

---

## Arquitectura del Sistema

### Patrón MVT (Model-View-Template)

Puddle sigue el patrón arquitectónico MVT de Django:

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│   URLs      │ ← Enrutamiento
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Views     │ ← Lógica de negocio
└──────┬──────┘
       │
       ├──────────┐
       ▼          ▼
┌──────────┐  ┌──────────┐
│  Models  │  │Templates │
│ (DB ORM) │  │  (HTML)  │
└──────────┘  └──────────┘
```

### Estructura de Aplicaciones

El proyecto está dividido en 4 aplicaciones Django:

1. **core**: Funcionalidades principales (home, auth, contacto)
2. **item**: Gestión de artículos y categorías
3. **conversation**: Sistema de mensajería
4. **dashboard**: Panel de control del usuario

---

## Modelos de Datos

### Diagrama de Relaciones

```
┌──────────────┐
│     User     │ (Django Auth)
└───────┬──────┘
        │
        │ 1:N
        ▼
┌──────────────┐      N:1     ┌──────────────┐
│     Item     │◄──────────────┤   Category   │
└───────┬──────┘               └──────────────┘
        │
        │ 1:N
        ▼
┌──────────────┐
│ Conversation │◄──── M:N ────► User (members)
└───────┬──────┘
        │
        │ 1:N
        ▼
┌──────────────┐      N:1     ┌──────────────┐
│ConversationMsg│◄─────────────┤     User     │
└──────────────┘               └──────────────┘
```

### Category (item/models.py)

**Propósito**: Clasificación de artículos

```python
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name']),
        ]
```

**Campos**:
- `name`: Nombre de la categoría (ej: "Electrónica", "Ropa")

**Índices**:
- `name`: Optimiza búsquedas y ordenamiento por nombre

**Métodos**:
- `__str__()`: Retorna el nombre de la categoría

**Relaciones**:
- `items`: Relación inversa con Item (1:N)

---

### Item (item/models.py)

**Propósito**: Representar artículos en venta

```python
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_sold', 'created_at']),
            models.Index(fields=['category', 'is_sold']),
            models.Index(fields=['created_by', 'created_at']),
            models.Index(fields=['is_sold', 'category', 'created_at']),
            models.Index(fields=['name']),
        ]
    
    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'El precio debe ser mayor a 0'})
        if self.price is not None and self.price > Decimal('99999999.99'):
            raise ValidationError({'price': 'El precio no puede exceder 99,999,999.99'})
```

**Campos**:
- `category`: Categoría del artículo (FK)
- `name`: Nombre del producto
- `description`: Descripción detallada (opcional)
- `price`: Precio en formato Decimal (max_digits=10, decimal_places=2)
- `image`: Imagen del producto (almacenada en media/item_images/)
- `is_sold`: Estado de venta (True/False)
- `created_by`: Usuario que creó el artículo (FK)
- `created_at`: Fecha de creación automática

**Índices de Base de Datos**:
- `is_sold + created_at`: Optimiza listado de items disponibles ordenados por fecha
- `category + is_sold`: Optimiza filtrado por categoría de items disponibles
- `created_by + created_at`: Optimiza dashboard del usuario
- `is_sold + category + created_at`: Índice compuesto para búsquedas complejas
- `name`: Optimiza búsquedas por nombre

**Relaciones**:
- `category`: N:1 con Category
- `created_by`: N:1 con User
- `conversations`: Relación inversa con Conversation (1:N)

**Validaciones**:
- `name`: Máximo 255 caracteres
- `price`: Debe ser mayor a 0 y no exceder 99,999,999.99
- `price`: Máximo 2 decimales
- `image`: Máximo 5MB, formatos: jpg, jpeg, png, gif, webp
- `price`: Debe ser un número válido
- `image`: Solo archivos de imagen

---

### Conversation (conversation/models.py)

**Propósito**: Gestionar conversaciones entre usuarios sobre un artículo

```python
class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-modified_at',)
        indexes = [
            models.Index(fields=['-modified_at']),
            models.Index(fields=['item', '-modified_at']),
            models.Index(fields=['created_at']),
        ]
```

**Campos**:
- `item`: Artículo sobre el que se conversa (FK)
- `members`: Usuarios participantes (M2M)
- `created_at`: Fecha de creación
- `modified_at`: Última actualización (se actualiza automáticamente)

**Índices de Base de Datos**:
- `modified_at DESC`: Optimiza listado de conversaciones por actividad reciente
- `item + modified_at DESC`: Optimiza búsqueda de conversaciones por item
- `created_at`: Optimiza ordenamiento por fecha de creación

**Relaciones**:
- `item`: N:1 con Item
- `members`: M:N con User
- `messages`: Relación inversa con ConversationMessage (1:N)

**Ordenamiento**:
- Por defecto: Conversaciones más recientes primero

---

### ConversationMessage (conversation/models.py)

**Propósito**: Mensajes individuales dentro de una conversación

```python
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['created_by', 'created_at']),
        ]
```

**Campos**:
- `conversation`: Conversación a la que pertenece (FK)
- `content`: Contenido del mensaje
- `created_at`: Fecha de envío
- `created_by`: Usuario que envió el mensaje (FK)

**Índices de Base de Datos**:
- `conversation + created_at`: Optimiza carga de mensajes en orden cronológico
- `created_by + created_at`: Optimiza búsqueda de mensajes por usuario

**Relaciones**:
- `conversation`: N:1 con Conversation
- `created_by`: N:1 con User

---

## Vistas y Lógica de Negocio

### Core Views (core/views.py)

#### `index(request)`
**Propósito**: Página principal del sitio

**Lógica**:
1. Obtiene los 6 artículos más recientes no vendidos
2. Obtiene todas las categorías
3. Renderiza la página principal

**Template**: `core/index.html`

**Contexto**:
```python
{
    'items': QuerySet[Item],      # Últimos 6 items
    'categories': QuerySet[Category]
}
```

---

#### `signup(request)`
**Propósito**: Registro de nuevos usuarios

**Flujo**:
```
GET  → Muestra formulario vacío
POST → Valida datos
     → Si válido: Crea usuario y redirige a login
     → Si inválido: Muestra errores
```

**Validaciones**:
- Username único
- Email válido
- Contraseñas coinciden
- Contraseña cumple requisitos de seguridad

**Template**: `core/signup.html`

---

#### `logout_view(request)`
**Propósito**: Cerrar sesión del usuario

**Lógica**:
1. Cierra la sesión con `logout(request)`
2. Obtiene items y categorías
3. Renderiza página principal

**Nota**: No usa redirect, renderiza directamente

---

#### `enviar_correo(request)`
**Propósito**: Enviar email de contacto

**Flujo**:
```
POST → Obtiene email del formulario
     → Envía email de confirmación
     → Maneja excepciones silenciosamente
     → Renderiza página principal
```

**Configuración Email**:
- SMTP: Gmail
- Puerto: 587
- TLS: Habilitado

---

### Item Views (item/views.py)

#### `items(request)`
**Propósito**: Listar y buscar artículos

**Parámetros GET**:
- `query`: Texto de búsqueda (opcional)
- `category`: ID de categoría (opcional)

**Lógica de Búsqueda**:
```python
# Base: Solo items no vendidos
items = Item.objects.filter(is_sold=False)

# Filtro por categoría
if category_id:
    items = items.filter(category_id=category_id)

# Búsqueda por texto (nombre O descripción)
if query:
    items = items.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    )
```

**Template**: `item/items.html`

---

#### `detail(request, pk)`
**Propósito**: Mostrar detalle de un artículo

**Lógica**:
1. Obtiene el item o retorna 404
2. Busca 3 items relacionados (misma categoría, no vendidos, excluyendo el actual)
3. Renderiza detalle

**Template**: `item/detail.html`

**Contexto**:
```python
{
    'item': Item,
    'related_items': QuerySet[Item]  # Máximo 3
}
```

---

#### `new(request)` 🔒
**Propósito**: Crear nuevo artículo

**Decorador**: `@login_required`

**Flujo POST**:
```
1. Valida formulario (NewItemForm)
2. Guarda sin commit (commit=False)
3. Asigna created_by = request.user
4. Guarda en BD
5. Redirige a detalle del item
```

**Archivos**:
- Maneja `request.FILES` para la imagen
- Imagen se guarda en `media/item_images/`

**Template**: `item/form.html`

---

#### `edit(request, pk)` 🔒
**Propósito**: Editar artículo existente

**Decorador**: `@login_required`

**Seguridad**:
```python
# Solo el creador puede editar
item = get_object_or_404(Item, pk=pk, created_by=request.user)
```

**Campos Editables**:
- name
- description
- price
- image
- is_sold

**Template**: `item/form.html`

---

#### `delete(request, pk)` 🔒
**Propósito**: Eliminar artículo

**Decorador**: `@login_required`

**Seguridad**:
- Solo el creador puede eliminar
- Verificación con `created_by=request.user`

**Efecto Cascada**:
- Elimina conversaciones asociadas
- Elimina mensajes de esas conversaciones
- Elimina imagen del sistema de archivos

---

### Conversation Views (conversation/views.py)

#### `new_conversation(request, item_pk)` 🔒
**Propósito**: Iniciar conversación sobre un artículo

**Validaciones**:
1. **No puede contactarse a sí mismo**:
```python
if item.created_by == request.user:
    return redirect('dashboard:index')
```

2. **Previene conversaciones duplicadas**:
```python
conversations = Conversation.objects.filter(
    item=item
).filter(members__in=[request.user.id])

if conversations.exists():
    return redirect('conversation:detail', pk=conversations.first().id)
```

**Flujo de Creación**:
```
1. Crea Conversation
2. Agrega request.user como member
3. Agrega item.created_by como member
4. Guarda conversación
5. Crea primer mensaje
6. Redirige a detalle del item
```

**Template**: `conversation/new.html`

---

#### `inbox(request)` 🔒
**Propósito**: Bandeja de entrada de conversaciones

**Lógica**:
```python
conversations = Conversation.objects.filter(
    members__in=[request.user.id]
)
```

**Ordenamiento**: Por `modified_at` descendente (más recientes primero)

**Template**: `conversation/inbox.html`

---

#### `detail(request, pk)` 🔒
**Propósito**: Ver y responder en una conversación

**Seguridad**:
```python
# Solo miembros pueden ver la conversación
conversation = get_object_or_404(
    Conversation, 
    pk=pk, 
    members=request.user
)
```

**Flujo POST** (enviar mensaje):
```
1. Valida formulario
2. Crea mensaje sin commit
3. Asigna conversation y created_by
4. Guarda mensaje
5. Actualiza modified_at de conversation
6. Recarga página
```

**Template**: `conversation/detail.html`

---

#### `eliminar_mensaje(request, message_id)` 🔒
**Propósito**: Eliminar mensaje propio

**Seguridad**:
```python
# Solo el creador puede eliminar
message = get_object_or_404(
    ConversationMessage, 
    pk=message_id, 
    created_by=request.user
)
```

**Método**: Solo POST

**Redirección**: Vuelve a la conversación

---

### Dashboard Views (dashboard/views.py)

#### `index(request)` 🔒
**Propósito**: Panel de control del usuario

**Lógica**:
```python
items = Item.objects.filter(created_by=request.user)
```

**Muestra**:
- Todos los artículos del usuario
- Vendidos y no vendidos
- Con opciones de editar/eliminar

**Template**: `dashboard/index.html`

---

### Auth Views (core/views_auth.py)

#### `CustomPasswordResetView`
**Propósito**: Solicitar reset de contraseña

**Configuración**:
- `email_template_name`: Template del email
- `success_url`: Página de confirmación

**Proceso**:
1. Usuario ingresa email
2. Sistema envía email con link
3. Link válido por 24 horas

---

#### `CustomPasswordResetConfirmView`
**Propósito**: Confirmar nueva contraseña

**Validaciones**:
- Token válido
- Contraseñas coinciden
- Cumple requisitos de seguridad

---

#### `CustomPasswordResetCompleteView`
**Propósito**: Confirmación de reset exitoso

**Template**: `core/password_reset_complete.html`

---

## Formularios

### SignupForm (core/forms.py)

**Hereda de**: `UserCreationForm`

**Campos**:
```python
- username: TextInput
- email: EmailInput
- password1: PasswordInput
- password2: PasswordInput (confirmación)
```

**Validaciones Automáticas**:
- Username único
- Email válido
- Contraseñas coinciden
- Longitud mínima de contraseña
- No puede ser similar al username
- No puede ser completamente numérica
- No puede ser una contraseña común

**Estilos**: Tailwind CSS (`w-full py-4 px-6 rounded-xl`)

---

### LoginForm (core/forms.py)

**Hereda de**: `AuthenticationForm`

**Campos**:
```python
- username: TextInput
- password: PasswordInput
```

**Validación**: Verifica credenciales contra la BD

---

### NewItemForm (item/forms.py)

**Modelo**: `Item`

**Campos**:
```python
- category: Select
- name: TextInput
- description: Textarea
- price: TextInput
- image: FileInput
```

**Validaciones**:
- Todos los campos requeridos excepto description e image
- Price debe ser numérico
- Image debe ser archivo de imagen válido

---

### EditItemForm (item/forms.py)

**Modelo**: `Item`

**Campos**:
```python
- name: TextInput
- description: Textarea
- price: TextInput
- image: FileInput
- is_sold: CheckboxInput
```

**Diferencia con NewItemForm**:
- No incluye `category` (no se puede cambiar)
- Incluye `is_sold` (marcar como vendido)

---

### ConversationMessageForm (conversation/forms.py)

**Modelo**: `ConversationMessage`

**Campos**:
```python
- content: Textarea
```

**Uso**:
- Crear nueva conversación
- Responder en conversación existente

---

## Sistema de Autenticación

### Configuración (settings.py)

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### Decoradores

**@login_required**:
- Protege vistas que requieren autenticación
- Redirige a LOGIN_URL si no autenticado
- Guarda URL original para redirigir después del login

**Vistas Protegidas**:
- Crear/editar/eliminar items
- Dashboard
- Conversaciones
- Eliminar mensajes

### Validadores de Contraseña

```python
AUTH_PASSWORD_VALIDATORS = [
    'UserAttributeSimilarityValidator',  # No similar a username
    'MinimumLengthValidator',            # Mínimo 8 caracteres
    'CommonPasswordValidator',           # No contraseñas comunes
    'NumericPasswordValidator',          # No solo números
]
```

### Recuperación de Contraseña

**Flujo**:
```
1. Usuario ingresa email
2. Sistema genera token único
3. Envía email con link
4. Usuario hace clic en link
5. Ingresa nueva contraseña
6. Token se invalida
```

**Seguridad**:
- Token válido por 24 horas
- Un solo uso
- Encriptado en URL

---

## Sistema de Mensajería

### Arquitectura

```
Item (Producto)
    ↓
Conversation (Conversación)
    ├── Member 1 (Vendedor)
    ├── Member 2 (Comprador)
    └── Messages
        ├── Message 1
        ├── Message 2
        └── Message N
```

### Reglas de Negocio

1. **Una conversación por item por usuario**:
   - Si ya existe, redirige a la existente
   
2. **Dos miembros por conversación**:
   - Vendedor (created_by del item)
   - Comprador (quien inicia la conversación)

3. **No auto-contacto**:
   - El vendedor no puede contactarse a sí mismo

4. **Ordenamiento**:
   - Por última actividad (modified_at)

5. **Eliminación de mensajes**:
   - Solo el autor puede eliminar
   - No elimina la conversación

### Actualización de Timestamps

```python
# Al enviar mensaje
conversation.save()  # Actualiza modified_at automáticamente
```

---

## Gestión de Archivos

### Configuración (settings.py)

```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Estructura de Archivos

```
media/
└── item_images/
    ├── imagen1.jpg
    ├── imagen2.png
    └── ...
```

### Upload de Imágenes

**Modelo**:
```python
image = models.ImageField(upload_to='item_images', blank=True, null=True)
```

**Vista**:
```python
form = NewItemForm(request.POST, request.FILES)
```

**Template**:
```html
<form method="post" enctype="multipart/form-data">
    {{ form.image }}
</form>
```

### Validación de Imágenes

**Validaciones en Formularios**:
- Tamaño máximo: 5MB
- Formatos permitidos: jpg, jpeg, png, gif, webp
- Validación automática con Pillow

**Pillow** valida automáticamente:
- Formato de imagen válido
- Archivo no corrupto
- Integridad de la imagen

### Eliminación Automática de Imágenes

**✅ Implementado**: Las imágenes se eliminan automáticamente del sistema de archivos.

**Comportamiento**:

1. **Al eliminar un Item**:
   - La imagen se elimina automáticamente
   - No quedan archivos huérfanos
   - Implementado con signal `pre_delete`

2. **Al actualizar la imagen**:
   - La imagen antigua se elimina automáticamente
   - Solo se mantiene la nueva imagen
   - Implementado con signal `pre_save`

3. **Al eliminar sin imagen**:
   - No genera errores
   - Funciona normalmente

**Implementación**:
```python
@receiver(pre_delete, sender=Item)
def delete_item_image_on_delete(sender, instance, **kwargs):
    """Elimina la imagen cuando se elimina el Item"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Item)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Elimina la imagen antigua al actualizar"""
    if not instance.pk:
        return
    
    try:
        old_item = Item.objects.get(pk=instance.pk)
        if old_item.image and old_item.image != instance.image:
            if os.path.isfile(old_item.image.path):
                os.remove(old_item.image.path)
    except Item.DoesNotExist:
        pass
```

**Beneficios**:
- ✅ No hay archivos huérfanos
- ✅ Ahorro de espacio en disco
- ✅ Gestión automática sin intervención manual
- ✅ Manejo seguro de errores

---

## Configuración

### Variables de Entorno (.env)

```env
# Base de Datos
DB_NAME=nombre_bd
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=clave-secreta-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=app_password
```

### Configuración de Email

**Gmail**:
1. Habilitar verificación en 2 pasos
2. Generar App Password
3. Usar App Password en EMAIL_HOST_PASSWORD

**Configuración**:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### CSRF Protection

```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://localhost:8000',
    'https://tu-dominio.com',
]
```

---

## Base de Datos

### Configuración MySQL

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}
```

### Migraciones

**Crear migraciones**:
```bash
python manage.py makemigrations
```

**Aplicar migraciones**:
```bash
python manage.py migrate
```

**Ver SQL de migración**:
```bash
python manage.py sqlmigrate item 0001
```

### Índices y Optimizaciones

**✅ Implementado**: El sistema cuenta con índices optimizados en todos los modelos principales.

**Índices Actuales**:

**Item**:
- `is_sold + created_at`: Listado de items disponibles
- `category + is_sold`: Filtrado por categoría
- `created_by + created_at`: Dashboard del usuario
- `is_sold + category + created_at`: Búsquedas complejas
- `name`: Búsquedas por nombre

**Category**:
- `name`: Ordenamiento y búsqueda

**Conversation**:
- `modified_at DESC`: Inbox ordenado por actividad
- `item + modified_at DESC`: Conversaciones por item
- `created_at`: Ordenamiento por fecha de creación

**ConversationMessage**:
- `conversation + created_at`: Mensajes en orden cronológico
- `created_by + created_at`: Mensajes por usuario

**Beneficios**:
- Consultas hasta 10x más rápidas en tablas grandes
- Mejor rendimiento en paginación
- Optimización automática de filtros y ordenamientos

---

## API Endpoints

### Resumen de Endpoints

| Endpoint | Método | Auth | Descripción |
|----------|--------|------|-------------|
| `/` | GET | No | Página principal |
| `/signup/` | GET, POST | No | Registro |
| `/login/` | GET, POST | No | Login |
| `/logout/` | GET | Sí | Logout |
| `/items/` | GET | No | Listar items |
| `/items/new/` | GET, POST | Sí | Crear item |
| `/items/<pk>/` | GET | No | Detalle item |
| `/items/<pk>/edit/` | GET, POST | Sí | Editar item |
| `/items/<pk>/delete/` | POST | Sí | Eliminar item |
| `/inbox/` | GET | Sí | Conversaciones |
| `/inbox/<pk>/` | GET, POST | Sí | Ver conversación |
| `/inbox/new/<item_pk>/` | GET, POST | Sí | Nueva conversación |
| `/dashboard/` | GET | Sí | Panel usuario |

### Códigos de Respuesta

- **200 OK**: Solicitud exitosa
- **302 Found**: Redirección
- **404 Not Found**: Recurso no encontrado
- **403 Forbidden**: Sin permisos
- **500 Internal Server Error**: Error del servidor

---

## Mejoras Futuras

### Funcionalidades

- [ ] Sistema de favoritos
- [ ] Calificaciones y reseñas
- [ ] Notificaciones en tiempo real
- [ ] Chat en vivo con WebSockets
- [ ] Búsqueda avanzada con filtros
- [ ] Geolocalización de productos
- [ ] Sistema de ofertas
- [ ] Historial de compras
- [ ] Múltiples imágenes por producto
- [ ] Categorías anidadas

### Optimizaciones

- [ ] Caché de consultas frecuentes
- [ ] Paginación en listados
- [ ] Lazy loading de imágenes
- [ ] CDN para archivos estáticos
- [ ] Compresión de imágenes
- [ ] Índices de base de datos
- [ ] Query optimization con select_related

### Seguridad

- [ ] Rate limiting
- [ ] Two-factor authentication
- [ ] Logs de auditoría
- [ ] Encriptación de datos sensibles
- [ ] Validación de archivos más estricta
- [ ] Protección contra bots

---

**Última actualización**: Noviembre 2024
**Versión**: 1.0.0
