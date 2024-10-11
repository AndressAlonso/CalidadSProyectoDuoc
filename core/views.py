from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def GestProducto(request):
    return render(request, "gestionProductos.html")


def adminConfig(request):
    return render(request, "adminTemplate.html")
