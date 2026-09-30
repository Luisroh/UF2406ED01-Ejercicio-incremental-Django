from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import Categoria, Producto
from .forms import RegistroForm, CategoriaForm, ProductoForm

def home(request):
    return render(request, "home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect("home")
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = RegistroForm()
    
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
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect("categoria_lista")
    return render(request, "categorias/eliminar.html", {"categoria": categoria})

def producto_lista(request):
    # select_related para traer categoria y usuario de golpe
    productos = Producto.objects.select_related("categoria", "usuario").order_by("-fecha_creacion")
    return render(request, "productos/lista.html", {"productos": productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria", "usuario"), 
        pk=pk
    )
    return render(request, "productos/detalle.html", {"producto": producto})

@login_required
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            # commit=False para asignar el usuario antes de guardar
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("mis_products")
    else:
        form = ProductoForm()
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Nuevo producto"})

@login_required
def producto_editar(request, pk):
    # Seguridad: Solo el dueño puede encontrar el producto
    producto = get_object_or_404(Producto, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("mis_products")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Editar producto"})

@login_required
def producto_eliminar(request, pk):
    # Seguridad: Solo el dueño puede encontrar el producto
    producto = get_object_or_404(Producto, pk=pk, usuario=request.user)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("mis_products")
    return render(request, "productos/eliminar.html", {"producto": producto})

@login_required
def mis_products(request):
    # Filtramos estrictamente por el usuario actual
    productos = Producto.objects.filter(usuario=request.user).select_related("categoria").order_by("-fecha_creacion")
    return render(request, "productos/mis_products.html", {"productos": productos})