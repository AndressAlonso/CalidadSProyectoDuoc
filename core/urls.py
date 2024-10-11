from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('gestion/PRODUCTO', GestProducto, name="TuProducto"),
    path('gestion/ADMIN', adminConfig, name="adminConfig"),
]
