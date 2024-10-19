from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.timezone import now
from django.db.models import Count
from datetime import timedelta
from .models import Producto
from .forms import ProductoFilterForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from datetime import timedelta
from django.utils.timezone import now

def home(request):
    messages.success(request, "Bienvenido a la página de inicio.")
    querySet = request.GET.get("buscar") 
    productos = Producto.objects.all()
    for producto in productos:
        if producto.proveedor == 'SemillasOrganicas.cl':
            producto.inventario = True
            producto.save()
    if querySet:
        productos = productos.filter(
            Q(nombre__icontains=querySet) | 
            Q(descripcion__icontains=querySet)
        ).distinct()

    form = ProductoFilterForm(request.GET)
    if form.is_valid():
        fecha_subida = form.cleaned_data.get('fecha_subida')
        if fecha_subida and fecha_subida != '-1':
            if fecha_subida == 'mes':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=30))
            elif fecha_subida == 'dia':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=1))
            elif fecha_subida == 'ano':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=365))

        tipo = form.cleaned_data.get('tipo')
        if tipo and tipo != '-1':
            productos = productos.filter(tipo=tipo)
            
        ordenar = form.cleaned_data.get('ordenar')
        if ordenar and ordenar == '-1':
            if ordenar == 'precio_desc':
                productos = productos.order_by('-precio')
            elif ordenar == 'precio_asc':
                productos = productos.order_by('precio')
            elif ordenar == 'vendidos_desc':
                productos = productos.annotate(vendidos=Count('id')).order_by('-vendidos')
            elif ordenar == 'vendidos_asc':
                productos = productos.annotate(vendidos=Count('id')).order_by('vendidos')
    print(request.GET.get("ordenar"))
    return render(request, "index.html", {'productos': productos, 'usuario': 'admin', 'form': form})



def GestProducto(request):
    productos = Producto.objects.filter(proveedor=request.user.usuario)
    tiposSemillas = TipoSemilla.objects.all()
    tiposInsumo = TipoInsumo.objects.all()
    tiposOrigen = tipoOrigen.objects.all() 
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nombre = request.POST.get('nombreProducto')
        stock = request.POST.get('stock')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        tipoProducto = request.POST.get('tipoProducto')
        tiposemilla_id = request.POST.get('tiposemilla')
        tipoinsumo_id = request.POST.get('tipoInsumo')
        origen_id = request.POST.get('origen')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        imagenUrl = ''

        # if not all([nombre, stock, precio, tipoProducto, descripcion]) or (tipoProducto == 'semilla' and not tiposemilla_id) or (tipoProducto == 'insumo' and not tipoinsumo_id):
        #     messages.error(request, "Por favor, completa todos los campos obligatorios.")
        #     return redirect('GestProducto')

        # Handle image upload
        if imagen:
            fs = FileSystemStorage(location='core\static\imgs')  # You can customize the storage location
            filename = fs.save(imagen.name, imagen)
            imagenUrl = fs.url(filename)

        # Handle optional fields
        origen = get_object_or_404(tipoOrigen, id=origen_id) if origen_id else None
        tipoSemilla = get_object_or_404(TipoSemilla, id=tiposemilla_id) if tipoProducto == 'semilla' and tiposemilla_id else None
        tipoInsumo = get_object_or_404(TipoInsumo, id=tipoinsumo_id) if tipoProducto == 'insumo' and tipoinsumo_id else None

        if producto_id:  # Edit existing product
            producto = get_object_or_404(Producto, id=producto_id)
            # Update the product
            producto.nombre = nombre
            producto.stock = stock
            producto.precio = precio
            producto.cantidad = cantidad
            producto.tipo = tipoProducto
            producto.origen = origen
            producto.descripcion = descripcion
            producto.tipoSemilla = tipoSemilla
            producto.tipoInsumo = tipoInsumo
            if imagenUrl:
                producto.imagenUrl = imagenUrl
            producto.save()
            messages.success(request, "Producto actualizado exitosamente.")
        else:  # Create new product
            # Create and save the product
            producto = Producto(
                nombre=nombre,
                stock=stock,
                precio=precio,
                cantidad=cantidad,
                tipo=tipoProducto,
                origen=origen,
                imagenUrl=imagenUrl,
                proveedor=request.user.usuario,
                tipoSemilla=tipoSemilla,
                tipoInsumo=tipoInsumo,
                descripcion=descripcion
            )
            producto.save()
            messages.success(request, "Producto agregado exitosamente.")

        return redirect('GestProducto')

    form = ProductoFilterForm(request.GET)
    if form.is_valid():
        fecha_subida = form.cleaned_data.get('fecha_subida')
        print(f"Filtering by fecha_subida: {fecha_subida}")  # Debug
        if fecha_subida and fecha_subida != '-1':
            if fecha_subida == 'mes':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=30))
            elif fecha_subida == 'dia':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=1))
            elif fecha_subida == 'ano':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=365))
        print(productos)  # Debug

        tipo = form.cleaned_data.get('tipo')
        print(f"Filtering by tipo: {tipo}")  # Debug
        if tipo and tipo != '-1':
            productos = productos.filter(tipo=tipo)
        print(productos)  # Debug

        ordenar = form.cleaned_data.get('ordenar')
        print(f"Ordering by: {ordenar}")  # Debug
        if ordenar == 'precio_desc':
            productos = productos.order_by('-precio')
        elif ordenar == 'precio_asc':
            productos = productos.order_by('precio')
        elif ordenar == 'vendidos_desc':
            productos = productos.annotate(vendidos=Count('id')).order_by('-vendidos')
        elif ordenar == 'vendidos_asc':
            productos = productos.annotate(vendidos=Count('id')).order_by('vendidos')
        print(productos) 

    return render(request, "gestionProductos.html", {
        'productos': productos,
        'semillas': tiposSemillas,
        'insumos': tiposInsumo,
        'origenes': tiposOrigen
    })

def detalle(request,id):
    producto = Producto.objects.get(id=id)
    return render(request, "detalle.html", {"producto": producto})

def carro(request):
    return render(request, "carro.html")

def adminConfig(request):
    productos = Producto.objects.all()
    tiposSemillas = TipoSemilla.objects.all()
    tiposInsumo = TipoInsumo.objects.all()
    tiposOrigen = tipoOrigen.objects.all() 
    filtro = request.GET.get('filtro')  # Capturamos la opción seleccionada
    productos = Producto.objects.all()  # Obtenemos todos los productos por defecto

    # Aplicamos los filtros según la selección del usuario
    if filtro == 'inventario':
        productos = productos.filter(inventario=True)  # Filtra productos con inventario=True
    elif filtro == 'ventas':
        productos = productos.filter(cantidadVentas__gt=1)  # Filtra productos con cantidad_ventas > 1
    elif filtro == 'todos':
        productos = productos 
    
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nombre = request.POST.get('nombreProducto')
        stock = request.POST.get('stock')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        tipoProducto = request.POST.get('tipoProducto')
        tiposemilla_id = request.POST.get('tiposemilla')
        tipoinsumo_id = request.POST.get('tipoInsumo')
        origen_id = request.POST.get('origen')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        imagenUrl = ''

        # if not all([nombre, stock, precio, tipoProducto, descripcion]) or (tipoProducto == 'semilla' and not tiposemilla_id) or (tipoProducto == 'insumo' and not tipoinsumo_id):
        #     messages.error(request, "Por favor, completa todos los campos obligatorios.")
        #     return redirect('GestProducto')

        # Handle image upload
        if imagen:
            fs = FileSystemStorage(location='core\static\imgs')  # You can customize the storage location
            filename = fs.save(imagen.name, imagen)
            imagenUrl = fs.url(filename)

        # Handle optional fields
        origen = get_object_or_404(tipoOrigen, id=origen_id) if origen_id else None
        tipoSemilla = get_object_or_404(TipoSemilla, id=tiposemilla_id) if tipoProducto == 'semilla' and tiposemilla_id else None
        tipoInsumo = get_object_or_404(TipoInsumo, id=tipoinsumo_id) if tipoProducto == 'insumo' and tipoinsumo_id else None

        if producto_id:  # Edit existing product
            producto = get_object_or_404(Producto, id=producto_id)
            # Update the product
            producto.nombre = nombre
            producto.stock = stock
            producto.precio = precio
            producto.cantidad = cantidad
            producto.tipo = tipoProducto
            producto.origen = origen
            producto.descripcion = descripcion
            producto.tipoSemilla = tipoSemilla
            producto.tipoInsumo = tipoInsumo
            if imagenUrl:
                producto.imagenUrl = imagenUrl
            producto.save()
            messages.success(request, "Producto actualizado exitosamente.")
        else:  # Create new product
            # Create and save the product
            producto = Producto(
                nombre=nombre,
                stock=stock,
                precio=precio,
                cantidad=cantidad,
                tipo=tipoProducto,
                origen=origen,
                imagenUrl=imagenUrl,
                proveedor=request.user.usuario,
                tipoSemilla=tipoSemilla,
                tipoInsumo=tipoInsumo,
                descripcion=descripcion
            )
            producto.save()
            messages.success(request, "Producto agregado exitosamente.")
        return redirect('adminConfig')

    # Apply filters if GET request
    form = ProductoFilterForm(request.GET)
    if form.is_valid():
        fecha_subida = form.cleaned_data.get('fecha_subida')
        if fecha_subida and fecha_subida != '-1':
            if fecha_subida == 'mes':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=30))
            elif fecha_subida == 'dia':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=1))
            elif fecha_subida == 'ano':
                productos = productos.filter(fechasubida__gte=now() - timedelta(days=365))

        tipo = form.cleaned_data.get('tipo')
        if tipo and tipo != '-1':
            productos = productos.filter(tipo=tipo)

        ordenar = form.cleaned_data.get('ordenar')
        if ordenar == 'precio_desc':
            productos = productos.order_by('-precio')
        elif ordenar == 'precio_asc':
            productos = productos.order_by('precio')
        elif ordenar == 'vendidos_desc':
            productos = productos.annotate(vendidos=Count('id')).order_by('-vendidos')
        elif ordenar == 'vendidos_asc':
            productos = productos.annotate(vendidos=Count('id')).order_by('vendidos')

    
    return render(request, "AdminTemplate.html", {
        'productos': productos,
        'semillas': tiposSemillas,
        'insumos': tiposInsumo,
        'origenes': tiposOrigen
    })


def addToCar(request, id):
    producto = Producto.objects.get(id=id)
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            item["cantidad"] += 1
            item["subtotal"] = item["cantidad"] * item["precio"]
            break
    else:
        carrito.append(
            {
                "id": id,
                "tipo": producto.tipo,
                "stock": producto.stock,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "subtotal": producto.precio,
                "proveedor": producto.proveedor.usuario.username,
                "origen": producto.origen.tipo,
                "cantidadProducto": producto.cantidad,
                "cantidad": 1,
                "imagenUrl": producto.imagenUrl,

            }
        )
    request.session["carrito"] = carrito
    return render(request, "carro.html")

def delToCar(request, id):
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1
                item["subtotal"] = item["cantidad"] * item["precio"]
                break
    else:
        carrito.remove(item)
    request.session["carrito"] = carrito
    return render(request, "carro.html")

def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('GestProducto') 


def crearProducto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        cantidad = request.POST.get('cantidad')
        tipo = request.POST.get('tipo')
        origen = request.POST.get('origen')
        imagenUrl = request.POST.get('imagenUrl')
        proveedor = request.user.usuario
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, cantidad=cantidad, tipo=tipo, origen=origen, imagenUrl=imagenUrl, proveedor=proveedor)
        producto.save()
        return redirect(request,'gestionProductos.html')
    return render(request, "gestionProductos.html")
