from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", home, name="home"),
    path("gestion/producto", GestProducto, name="GestProducto"),
    path("gestion/admin", adminConfig, name="adminConfig"),
    path("Carrito", carro, name="carrito"),
    path("addToCar/<int:id>", addToCar, name="addToCar"),
    path("delToCar/<int:id>/", delToCar, name="delToCar"),
    path("producto/detalle/<int:id>", detalle, name="detalle"),
    path("eliminarProducto/<int:id>", eliminarProducto, name="eliminarProducto"),
    path('comprar', comprar, name="comprar"),
    path('comprarUnProducto/<int:id>', comprarUnProducto, name="comprarUnProducto"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', register, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
