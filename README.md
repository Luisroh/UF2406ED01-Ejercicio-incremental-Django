# Tienda Django - Proyecto de Prueba Práctica

**Autor:** Luis Robert Huertas Araya  
**Módulo:** UF2406 - Desarrollo de Aplicaciones Web con Django  
**Descripción:** Aplicación web completa tipo "Tienda" desarrollada con Django 5, Bootstrap 5 y SQLite. Implementa un sistema CRUD con autenticación, autorización, propiedad de recursos y roles de usuario.

---

## 📋 Índice
1. [Descripción General](#-descripción-general)
2. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
3. [Funcionalidades Principales](#-funcionalidades-principales)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
6. [Roles y Permisos](#-roles-y-permisos)
7. [Conceptos Aplicados](#-conceptos-aplicados)
8. [Pruebas Recomendadas](#-pruebas-recomendadas)

---

## 📖 Descripción General

Este proyecto es una aplicación web desarrollada como práctica final del módulo. Consiste en una **tienda online** donde los usuarios pueden registrarse, iniciar sesión, crear productos, gestionarlos y ver los productos de otros usuarios. 

El objetivo principal es demostrar el dominio de los conceptos fundamentales de Django, incluyendo:
- Vistas basadas en funciones (FBV).
- Autenticación y autorización de usuarios.
- Relaciones entre modelos (ForeignKey).
- CRUD completo (Crear, Leer, Actualizar, Eliminar).
- Sistema de permisos y roles (Usuario normal vs. Administrador).
- Uso de Bootstrap 5 para una interfaz moderna y responsive.
- Gestión de mensajes (alertas de éxito/error).

---

## 🛠 Tecnologías Utilizadas

- **Backend:** Python 3.12+, Django 5.2.17
- **Base de Datos:** SQLite 3 (por defecto en desarrollo)
- **Frontend:** HTML5, CSS3, Bootstrap 5.3.3, JavaScript (Bootstrap Bundle)
- **Autenticación:** Sistema nativo de Django (`django.contrib.auth`)
- **Gestión de Formularios:** `ModelForm` + Mixin personalizado para Bootstrap
- **Correo Electrónico:** Backend de consola para recuperación de contraseña

---

## ✨ Funcionalidades Principales

### 1. Gestión de Usuarios
- **Registro:** Creación de cuentas con validación de email único.
- **Login / Logout:** Inicio y cierre de sesión seguro.
- **Recuperación de contraseña:** Flujo completo con envío de token por email (simulado en consola) y cambio de contraseña.

### 2. CRUD de Categorías
- Crear, listar, editar y eliminar categorías.
- Cada categoría tiene un nombre y una descripción.
- Al eliminar una categoría, se eliminan sus productos asociados (CASCADE).

### 3. CRUD de Productos
- **Listado general:** Todos los productos visibles para cualquier usuario.
- **Mis productos:** Vista filtrada que muestra solo los productos creados por el usuario logueado.
- **Creación:** El producto se asigna automáticamente al usuario que lo crea.
- **Edición/Eliminación:** Solo el propietario o un administrador pueden editar/eliminar el producto.
- **Detalle:** Vista pública con información completa del producto y su propietario.

### 4. Panel de Administración Interno
- Accesible solo para usuarios con `is_staff = True`.
- Muestra estadísticas (total de usuarios y productos).
- Tabla con todos los productos del sistema y acciones rápidas.

### 5. Interfaz de Usuario
- Navbar responsive con Bootstrap 5.
- Alertas de éxito/error al realizar acciones (crear, editar, eliminar).
- Badges que indican el rol del usuario (Usuario / Administrador).
- Formularios estilizados automáticamente mediante un Mixin de Bootstrap.

---

## 📂 Estructura del Proyecto

    tienda/
    ├── .venv/                      # Entorno virtual
    ├── productos/                  # App principal
    │   ├── migrations/             # Migraciones de la base de datos
    │   ├── templates/              # Templates de la app
    │   │   ├── administracion/     # Panel de admin interno
    │   │   ├── categorias/         # CRUD de categorías
    │   │   ├── productos/          # CRUD de productos
    │   │   └── registration/       # Login, registro, reset password
    │   ├── admin.py                # Configuración del admin de Django
    │   ├── apps.py
    │   ├── forms.py                # Formularios con Mixin de Bootstrap
    │   ├── models.py               # Modelos Categoria y Producto
    │   ├── permissions.py          # Lógica centralizada de permisos
    │   ├── urls.py                 # Rutas de la app
    │   └── views.py                # Vistas (FBV)
    ├── tienda/                     # Configuración del proyecto
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── templates/                  # Templates globales
    │   ├── 403.html                # Error personalizado
    │   ├── 404.html                # Error personalizado
    │   ├── base.html               # Template base con navbar
    │   └── home.html               # Página principal
    ├── db.sqlite3                  # Base de datos
    ├── manage.py
    └── README.md

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio

    git clone <URL_DEL_REPOSITORIO>
    cd tienda

### 2. Crear y activar el entorno virtual

    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux / Mac
    python3 -m venv .venv
    source .venv/bin/activate

### 3. Instalar dependencias

    pip install django

### 4. Aplicar migraciones

    python manage.py makemigrations
    python manage.py migrate

### 5. Crear un superusuario (para acceder al admin de Django)

    python manage.py createsuperuser

### 6. Ejecutar el servidor

    python manage.py runserver

### 7. Acceder a la aplicación
- **Tienda:** http://127.0.0.1:8000/
- **Admin Django:** http://127.0.0.1:8000/admin/

---

## 🔐 Roles y Permisos

El sistema implementa tres niveles de acceso:

| Rol | `is_staff` | Puede crear | Puede editar | Puede eliminar | Accede al panel admin |
|-----|:----------:|:-----------:|:------------:|:--------------:|:---------------------:|
| **Visitante** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Usuario normal** | ❌ | ✅ | Solo sus productos | Solo sus productos | ❌ |
| **Administrador** | ✅ | ✅ | Cualquier producto | Cualquier producto | ✅ |

### Lógica de permisos
La lógica está centralizada en `productos/permissions.py`:

    def puede_editar_producto(user, producto):
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        return producto.usuario == user

### Seguridad en dos capas
1. **Backend (Vistas):** Se comprueba el permiso antes de procesar la acción. Si no se tiene permiso, se lanza `PermissionDenied` (error 403).
2. **Frontend (Templates):** Se ocultan los botones de editar/eliminar si el usuario no es el propietario ni staff.

> ⚠️ **Importante:** Ocultar botones en el HTML no es suficiente. La seguridad real está en las vistas, que impiden el acceso directo por URL.

---

## 🧠 Conceptos Aplicados

### Autenticación
- Uso de `request.user` para identificar al usuario.
- Decoradores `@login_required` y `@staff_member_required`.

### Autorización
- Comprobación de `producto.usuario == request.user`.
- Uso de `is_staff` para el rol de administrador.

### Propiedad de Recursos
- Relación `ForeignKey` entre `Producto` y `User`.
- Uso de `commit=False` para asignar el usuario antes de guardar.
- Uso de `related_name="productos"` para acceder a `user.productos.all()`.

### Formularios
- `ModelForm` para generar formularios automáticamente.
- Mixin `BootstrapFormMixin` para añadir clases CSS automáticamente.

### Mensajes
- Uso de `django.contrib.messages` para notificar al usuario sobre el resultado de sus acciones.

---

## 🧪 Pruebas Recomendadas

Para verificar el correcto funcionamiento del sistema, se recomienda realizar las siguientes pruebas:

### Preparación
1. Crea tres usuarios desde el admin de Django:
   - `juan` (is_staff = False)
   - `maria` (is_staff = False)
   - `admin` (is_staff = True)

### Prueba 1: Propiedad de productos
- Inicia sesión como **juan**.
- Crea un producto llamado "Portátil".
- Verifica que el propietario es `juan`.

### Prueba 2: Aislamiento entre usuarios
- Cierra sesión e inicia como **maria**.
- Ve a "Mis productos": NO debe aparecer "Portátil".
- Ve al listado general: SÍ debe aparecer "Portátil" (con el propietario `juan`).
- Intenta editar el producto de Juan escribiendo la URL a mano (`/productos/1/editar/`): debe dar error 403.

### Prueba 3: Permisos de administrador
- Inicia sesión como **admin**.
- Ve al listado general: debe ver los botones de "Editar" y "Eliminar" en TODOS los productos.
- Edita el producto de Juan: debe permitirlo.
- Accede al panel de administración (`/panel-admin/`): debe funcionar.

### Prueba 4: Recuperación de contraseña
- Cierra sesión.
- Ve a "Login" → "¿Has olvidado tu contraseña?".
- Introduce el email de un usuario.
- Revisa la consola del servidor: aparecerá el email con el enlace de recuperación.

---

## 📝 Notas Finales

Este proyecto ha sido desarrollado como parte de la evaluación del módulo **UF2406**, demostrando la capacidad de construir una aplicación web completa con Django, aplicando buenas prácticas de seguridad, organización de código y diseño de interfaz.

**Autor:** Luis Robert Huertas Araya  
**Fecha:** Septiembre 2026

---

## 📄 Licencia

Este proyecto es de uso educativo y forma parte de una práctica académica.