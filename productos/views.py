from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
# IMPORTANTE: Importamos el módulo de mensajes para las notificaciones
from django.contrib import messages 
from .models import Categoria, Producto
from .forms import RegistroForm, CategoriaForm, ProductoForm

def home(request):
    return render(request, "home.html")

def register(request):
    # Si el usuario ya está logueado, lo mandamos a casa
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            # Mensaje de éxito al registrar
            messages.success(request, "Usuario registrado correctamente.")
            return redirect("home")
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = RegistroForm()
    
    # Renderizamos el formulario (tanto si es GET como si es POST inválido)
    return render(request, "registration/register.html", {"form": form})

@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, "categorias/lista.html", {"categorias": categorias})

@login_required
def categoria_crear(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensaje de éxito al crear categoría
            messages.success(request, "Categoría creada correctamente.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm()
    return render(request, "categorias/formulario.html", {"form": form, "titulo": "Nueva categoría"})

@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            # Mensaje de éxito al editar
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "categorias/formulario.html", {"form": form, "titulo": "Editar categoría"})

@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        # Mensaje de éxito al eliminar
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect("categoria_lista")
    return render(request, "categorias/eliminar.html", {"categoria": categoria})

def producto_lista(request):
    # select_related mejora el rendimiento al traer la categoría asociada
    productos = Producto.objects.select_related("categoria")
    return render(request, "productos/lista.html", {"productos": productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})

@login_required
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensaje de éxito al crear producto
            messages.success(request, "Producto creado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm()
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Nuevo producto"})

@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Mensaje de éxito al editar producto
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Editar producto"})

@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        # Mensaje de éxito al eliminar producto
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("producto_lista")
    return render(request, "productos/eliminar.html", {"producto": producto})