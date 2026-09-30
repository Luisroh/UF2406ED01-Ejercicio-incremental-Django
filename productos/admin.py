from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "fecha_creacion")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "usuario", "precio", "fecha_creacion")
    list_filter = ("categoria", "usuario")
    search_fields = ("nombre", "usuario__username")