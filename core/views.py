from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    productos = Producto.objects.all()
    return render(request, "index.html", {'productos': productos, 'usuario': 'admin'})


def GestProducto(request):
    return render(request, "gestionProductos.html")


def adminConfig(request):
    return render(request, "adminTemplate.html")
