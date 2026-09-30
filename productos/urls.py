from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    
    # Categorías
    path("categorias/", views.categoria_lista, name="categoria_lista"),
    path("categorias/nueva/", views.categoria_crear, name="categoria_crear"),
    path("categorias/<int:pk>/editar/", views.categoria_editar, name="categoria_editar"),
    path("categorias/<int:pk>/eliminar/", views.categoria_eliminar, name="categoria_eliminar"),
    
    # Productos
    path("productos/", views.producto_lista, name="producto_lista"),
    path("mis-productos/", views.mis_products, name="mis_products"),
    path("productos/nuevo/", views.producto_crear, name="producto_crear"),
    path("productos/<int:pk>/", views.producto_detalle, name="producto_detalle"),
    path("productos/<int:pk>/editar/", views.producto_editar, name="producto_editar"),
    path("productos/<int:pk>/eliminar/", views.producto_eliminar, name="producto_eliminar"),
    
    # Punto 8: URL del panel de administración
    path("panel-admin/", views.panel_admin, name="panel_admin"),
]