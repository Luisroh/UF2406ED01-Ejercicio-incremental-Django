# productos/permissions.py

def puede_editar_producto(user, producto):
    """
    Devuelve True si el usuario puede editar el producto.
    - Debe estar autenticado.
    - Si es staff (administrador), puede editar cualquiera.
    - Si es usuario normal, solo puede editar los suyos.
    """
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return producto.usuario == user

def puede_eliminar_producto(user, producto):
    """
    Misma lógica que la edición para la eliminación.
    """
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return producto.usuario == user