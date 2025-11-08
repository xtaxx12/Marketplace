# 🔌 API Reference - Puddle Marketplace

Documentación completa de todos los endpoints disponibles en el sistema.

---

## 📑 Índice

- [Autenticación](#autenticación)
- [Items (Artículos)](#items-artículos)
- [Conversaciones](#conversaciones)
- [Dashboard](#dashboard)
- [Códigos de Estado](#códigos-de-estado)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Autenticación

### Registro de Usuario

**Endpoint**: `POST /signup/`

**Descripción**: Crear una nueva cuenta de usuario

**Autenticación**: No requerida

**Parámetros del Formulario**:
```json
{
  "username": "string (requerido, único)",
  "email": "string (requerido, formato email)",
  "password1": "string (requerido, mín 8 caracteres)",
  "password2": "string (requerido, debe coincidir con password1)"
}
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/login/`

**Errores Posibles**:
- Username ya existe
- Email inválido
- Contraseñas no coinciden
- Contraseña muy débil

**Ejemplo**:
```html
<form method="post" action="/signup/">
  {% csrf_token %}
  <input type="text" name="username" required>
  <input type="email" name="email" required>
  <input type="password" name="password1" required>
  <input type="password" name="password2" required>
  <button type="submit">Registrarse</button>
</form>
```

---

### Iniciar Sesión

**Endpoint**: `POST /login/`

**Descripción**: Autenticar usuario existente

**Autenticación**: No requerida

**Parámetros del Formulario**:
```json
{
  "username": "string (requerido)",
  "password": "string (requerido)"
}
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/` (o URL guardada en `next`)
- **Cookie**: `sessionid` (sesión de Django)

**Errores Posibles**:
- Credenciales inválidas
- Usuario no existe
- Cuenta desactivada

**Ejemplo con Next URL**:
```html
<form method="post" action="/login/?next=/dashboard/">
  {% csrf_token %}
  <input type="text" name="username">
  <input type="password" name="password">
  <button type="submit">Entrar</button>
</form>
```

---

### Cerrar Sesión

**Endpoint**: `GET /logout/`

**Descripción**: Cerrar sesión del usuario actual

**Autenticación**: Requerida

**Respuesta**:
- **Código**: 200 OK
- **Renderiza**: Página principal
- **Efecto**: Invalida sesión

---

### Recuperar Contraseña

#### Solicitar Reset

**Endpoint**: `POST /password_reset/`

**Descripción**: Solicitar link de recuperación

**Parámetros**:
```json
{
  "email": "string (requerido)"
}
```

**Respuesta**:
- **Código**: 302 (Redirect)
- **Redirección**: `/password_reset/done/`
- **Efecto**: Envía email con link

---

#### Confirmar Nueva Contraseña

**Endpoint**: `POST /reset/<uidb64>/<token>/`

**Descripción**: Establecer nueva contraseña

**Parámetros**:
```json
{
  "new_password1": "string (requerido)",
  "new_password2": "string (requerido)"
}
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/reset/done/`

---

## Items (Artículos)

### Listar Artículos

**Endpoint**: `GET /items/`

**Descripción**: Obtener lista de artículos disponibles

**Autenticación**: No requerida

**Parámetros Query**:
```
?query=texto          # Buscar en nombre y descripción
?category=id          # Filtrar por categoría
?query=laptop&category=1  # Combinar filtros
```

**Respuesta**:
- **Código**: 200 OK
- **Template**: `item/items.html`
- **Contexto**:
```python
{
  'items': QuerySet[Item],        # Items filtrados
  'categories': QuerySet[Category],
  'query': str,                   # Texto buscado
  'category_id': int              # ID categoría seleccionada
}
```

**Ejemplo de Búsqueda**:
```
GET /items/?query=laptop&category=1
```

---

### Detalle de Artículo

**Endpoint**: `GET /items/<int:pk>/`

**Descripción**: Ver detalles de un artículo específico

**Autenticación**: No requerida

**Parámetros URL**:
- `pk`: ID del artículo (integer)

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Template**: `item/detail.html`
- **Contexto**:
```python
{
  'item': Item,
  'related_items': QuerySet[Item]  # Máximo 3 items relacionados
}
```

**Respuesta Error**:
- **Código**: 404 Not Found (si el item no existe)

**Ejemplo**:
```
GET /items/42/
```

---

### Crear Artículo

**Endpoint**: `POST /items/new/`

**Descripción**: Publicar un nuevo artículo

**Autenticación**: ✅ Requerida

**Parámetros del Formulario**:
```json
{
  "category": "integer (requerido, ID de categoría)",
  "name": "string (requerido, max 255)",
  "description": "string (opcional)",
  "price": "float (requerido)",
  "image": "file (opcional, imagen)"
}
```

**Headers**:
```
Content-Type: multipart/form-data
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/items/<nuevo_id>/`

**Validaciones**:
- Usuario autenticado
- Categoría existe
- Precio es numérico positivo
- Imagen es archivo válido (si se proporciona)

**Ejemplo**:
```html
<form method="post" action="/items/new/" enctype="multipart/form-data">
  {% csrf_token %}
  <select name="category" required>
    <option value="1">Electrónica</option>
  </select>
  <input type="text" name="name" required>
  <textarea name="description"></textarea>
  <input type="number" step="0.01" name="price" required>
  <input type="file" name="image" accept="image/*">
  <button type="submit">Publicar</button>
</form>
```

---

### Editar Artículo

**Endpoint**: `POST /items/<int:pk>/edit/`

**Descripción**: Modificar artículo existente

**Autenticación**: ✅ Requerida

**Autorización**: Solo el creador del artículo

**Parámetros URL**:
- `pk`: ID del artículo

**Parámetros del Formulario**:
```json
{
  "name": "string (requerido)",
  "description": "string (opcional)",
  "price": "float (requerido)",
  "image": "file (opcional)",
  "is_sold": "boolean (opcional)"
}
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/items/<pk>/`

**Respuesta Error**:
- **Código**: 404 Not Found (si no es el propietario o no existe)

**Ejemplo**:
```
POST /items/42/edit/
```

---

### Eliminar Artículo

**Endpoint**: `POST /items/<int:pk>/delete/`

**Descripción**: Eliminar artículo permanentemente

**Autenticación**: ✅ Requerida

**Autorización**: Solo el creador del artículo

**Parámetros URL**:
- `pk`: ID del artículo

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/dashboard/`

**Efectos**:
- Elimina el artículo
- Elimina conversaciones asociadas
- Elimina mensajes de esas conversaciones
- **No elimina** la imagen del servidor (comportamiento actual)

**Ejemplo**:
```html
<form method="post" action="/items/42/delete/">
  {% csrf_token %}
  <button type="submit">Eliminar</button>
</form>
```

---

## Conversaciones

### Bandeja de Entrada

**Endpoint**: `GET /inbox/`

**Descripción**: Ver todas las conversaciones del usuario

**Autenticación**: ✅ Requerida

**Respuesta**:
- **Código**: 200 OK
- **Template**: `conversation/inbox.html`
- **Contexto**:
```python
{
  'conversations': QuerySet[Conversation]  # Ordenadas por modified_at DESC
}
```

**Ordenamiento**: Conversaciones más recientes primero

**Ejemplo**:
```
GET /inbox/
```

---

### Ver Conversación

**Endpoint**: `GET /inbox/<int:pk>/`

**Descripción**: Ver mensajes de una conversación

**Autenticación**: ✅ Requerida

**Autorización**: Solo miembros de la conversación

**Parámetros URL**:
- `pk`: ID de la conversación

**Respuesta Exitosa**:
- **Código**: 200 OK
- **Template**: `conversation/detail.html`
- **Contexto**:
```python
{
  'conversation': Conversation,
  'form': ConversationMessageForm
}
```

**Respuesta Error**:
- **Código**: 404 Not Found (si no es miembro o no existe)

---

### Enviar Mensaje

**Endpoint**: `POST /inbox/<int:pk>/`

**Descripción**: Enviar mensaje en conversación existente

**Autenticación**: ✅ Requerida

**Autorización**: Solo miembros de la conversación

**Parámetros URL**:
- `pk`: ID de la conversación

**Parámetros del Formulario**:
```json
{
  "content": "string (requerido)"
}
```

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/inbox/<pk>/`
- **Efecto**: Actualiza `modified_at` de la conversación

**Ejemplo**:
```html
<form method="post" action="/inbox/42/">
  {% csrf_token %}
  <textarea name="content" required></textarea>
  <button type="submit">Enviar</button>
</form>
```

---

### Iniciar Conversación

**Endpoint**: `POST /inbox/new/<int:item_pk>/`

**Descripción**: Crear nueva conversación sobre un artículo

**Autenticación**: ✅ Requerida

**Parámetros URL**:
- `item_pk`: ID del artículo

**Parámetros del Formulario**:
```json
{
  "content": "string (requerido, primer mensaje)"
}
```

**Validaciones**:
1. El artículo existe
2. No es el propietario del artículo
3. No existe conversación previa sobre este artículo

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/items/<item_pk>/`

**Respuestas Especiales**:
- Si es el propietario: Redirect a `/dashboard/`
- Si ya existe conversación: Redirect a `/inbox/<conversation_id>/`

**Efectos**:
- Crea Conversation
- Agrega 2 miembros (comprador y vendedor)
- Crea primer mensaje

**Ejemplo**:
```html
<form method="post" action="/inbox/new/42/">
  {% csrf_token %}
  <textarea name="content" placeholder="Hola, me interesa tu producto..." required></textarea>
  <button type="submit">Contactar Vendedor</button>
</form>
```

---

### Eliminar Mensaje

**Endpoint**: `POST /inbox/eliminar/<int:message_id>/`

**Descripción**: Eliminar mensaje propio

**Autenticación**: ✅ Requerida

**Autorización**: Solo el autor del mensaje

**Parámetros URL**:
- `message_id`: ID del mensaje

**Respuesta Exitosa**:
- **Código**: 302 (Redirect)
- **Redirección**: `/inbox/<conversation_id>/`

**Respuesta Error**:
- **Código**: 404 Not Found (si no es el autor o no existe)

**Nota**: No elimina la conversación, solo el mensaje

**Ejemplo**:
```html
<form method="post" action="/inbox/eliminar/123/">
  {% csrf_token %}
  <button type="submit">Eliminar</button>
</form>
```

---

## Dashboard

### Panel de Usuario

**Endpoint**: `GET /dashboard/`

**Descripción**: Ver artículos publicados por el usuario

**Autenticación**: ✅ Requerida

**Respuesta**:
- **Código**: 200 OK
- **Template**: `dashboard/index.html`
- **Contexto**:
```python
{
  'items': QuerySet[Item]  # Todos los items del usuario
}
```

**Incluye**:
- Artículos vendidos y no vendidos
- Opciones para editar/eliminar
- Estadísticas (si están implementadas)

**Ejemplo**:
```
GET /dashboard/
```

---

## Códigos de Estado

### Exitosos (2xx)

| Código | Descripción | Uso |
|--------|-------------|-----|
| 200 OK | Solicitud exitosa | GET requests |
| 302 Found | Redirección temporal | POST exitoso, redirects |

### Errores del Cliente (4xx)

| Código | Descripción | Cuándo Ocurre |
|--------|-------------|---------------|
| 400 Bad Request | Datos inválidos | Formulario con errores |
| 403 Forbidden | Sin permisos | Intentar editar item ajeno |
| 404 Not Found | Recurso no existe | Item/conversación no encontrada |

### Errores del Servidor (5xx)

| Código | Descripción | Cuándo Ocurre |
|--------|-------------|---------------|
| 500 Internal Server Error | Error del servidor | Excepción no manejada |

---

## Ejemplos de Uso

### Flujo Completo: Publicar y Vender

```python
# 1. Registro
POST /signup/
{
  "username": "vendedor123",
  "email": "vendedor@example.com",
  "password1": "MiPassword123!",
  "password2": "MiPassword123!"
}
→ Redirect a /login/

# 2. Login
POST /login/
{
  "username": "vendedor123",
  "password": "MiPassword123!"
}
→ Redirect a /

# 3. Crear artículo
POST /items/new/
{
  "category": 1,
  "name": "Laptop Dell XPS 15",
  "description": "Excelente estado, 16GB RAM",
  "price": 1200.00,
  "image": <archivo>
}
→ Redirect a /items/42/

# 4. Comprador inicia conversación
POST /inbox/new/42/
{
  "content": "Hola, ¿aún está disponible?"
}
→ Redirect a /items/42/

# 5. Vendedor responde
POST /inbox/1/
{
  "content": "Sí, está disponible. ¿Cuándo puedes recogerlo?"
}
→ Redirect a /inbox/1/

# 6. Marcar como vendido
POST /items/42/edit/
{
  "name": "Laptop Dell XPS 15",
  "description": "Excelente estado, 16GB RAM",
  "price": 1200.00,
  "is_sold": true
}
→ Redirect a /items/42/
```

---

### Búsqueda Avanzada

```python
# Buscar laptops en categoría Electrónica
GET /items/?query=laptop&category=1

# Buscar por descripción
GET /items/?query=16GB%20RAM

# Ver todas las categorías
GET /items/
```

---

### Gestión de Conversaciones

```python
# Ver todas mis conversaciones
GET /inbox/

# Ver conversación específica
GET /inbox/5/

# Enviar mensaje
POST /inbox/5/
{
  "content": "¿Aceptas pagos en efectivo?"
}

# Eliminar mi mensaje
POST /inbox/eliminar/123/
```

---

## Autenticación con CSRF

Todas las peticiones POST requieren token CSRF:

```html
<form method="post">
  {% csrf_token %}
  <!-- campos del formulario -->
</form>
```

En JavaScript:
```javascript
// Obtener token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Usar en fetch
fetch('/items/new/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': csrftoken,
  },
  body: formData
});
```

---

## Rate Limiting

**Actualmente no implementado**

Recomendaciones para producción:
- Limitar intentos de login: 5 por minuto
- Limitar creación de items: 10 por hora
- Limitar mensajes: 30 por minuto

---

## Paginación

**Actualmente no implementado**

Los listados retornan todos los resultados. Para grandes volúmenes de datos, se recomienda implementar paginación.

---

## Webhooks

**No disponible**

El sistema no ofrece webhooks actualmente.

---

## Versionado

**Versión Actual**: 1.0

No hay versionado de API. Cambios futuros se documentarán aquí.

---

**Última actualización**: Noviembre 2024
