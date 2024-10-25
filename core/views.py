from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.timezone import now
from django.db.models import Count
from datetime import timedelta, timezone
from .models import Producto
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)
            messages.success(request, 'Bienvenido!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registro.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success('Bienvenido ' + username + '!.')
            return redirect('home')
        else:
            messages.success(request, 'Contraseña o usuario Invalidos!.')
    return render(request, 'login.html')


def home(request):
    querySet = request.GET.get("buscar") 
    productos = Producto.objects.all()
    if querySet:
        productos = productos.filter(
            Q(nombre__icontains=querySet) | 
            Q(descripcion__icontains=querySet)
        ).distinct()

    fecha_subida = request.GET.get('fecha_subida', '-')
    tipo_producto = request.GET.get('tipo', '-')
    ordenar = request.GET.get('ordenar', '-')

    if fecha_subida == 'dia':
        productos = productos.filter(fechasubida=timezone.now().date())
    elif fecha_subida == 'mes':
        productos = productos.filter(fechasubida__month=timezone.now().month)
    elif fecha_subida == 'ano':
        productos = productos.filter(fechasubida__year=timezone.now().year)

    if tipo_producto == 'semilla':
        productos = productos.filter(tipo='semilla')
    elif tipo_producto == 'insumo':
        productos = productos.filter(tipo='insumo')

    if ordenar == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar == 'vendidos_desc':
        productos = productos.order_by('-cantidadVentas')
    elif ordenar == 'vendidos_asc':
        productos = productos.order_by('cantidadVentas')
    return render(request, "index.html", {'productos': productos})



def GestProducto(request):
    usuario = Usuario.objects.get(usuario=request.user)
    ventasUsuario = DetalleVenta.objects.filter(venta__proveedor=usuario)
    print(ventasUsuario)
    productos = Producto.objects.filter(proveedor=usuario)
    ventas = 0
    cantidadVentas = ventasUsuario.count()
    for p in ventasUsuario:
        ventas += p.cantidad * p.precio
        
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
        PAGINA = request.POST.get('paginaData')
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
        else:  
            producto = Producto(
                nombre=nombre,
                stock=stock,
                precio=precio,
                cantidad=cantidad,
                tipo=tipoProducto,
                origen=origen,
                imagenUrl=imagenUrl,
                proveedor=usuario,
                tipoSemilla=tipoSemilla,
                tipoInsumo=tipoInsumo,
                descripcion=descripcion
            )
            producto.save()
            messages.success(request, "Producto agregado exitosamente.")
        return redirect('GestProducto')
    fecha_subida = request.GET.get('fecha_subida', '-')
    tipo_producto = request.GET.get('tipo', '-')
    ordenar = request.GET.get('ordenar', '-')

    if fecha_subida == 'dia':
        productos = productos.filter(fechasubida=timezone.now().date())  # Comparación directa
    elif fecha_subida == 'mes':
        productos = productos.filter(fechasubida__month=timezone.now().month)
    elif fecha_subida == 'ano':
        productos = productos.filter(fechasubida__year=timezone.now().year)

    if tipo_producto == 'semilla':
        productos = productos.filter(tipo='semilla')
    elif tipo_producto == 'insumo':
        productos = productos.filter(tipo='insumo')

    if ordenar == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar == 'vendidos_desc':
        productos = productos.order_by('-vendidos')
    elif ordenar == 'vendidos_asc':
        productos = productos.order_by('vendidos')
    tiposSemillas = TipoSemilla.objects.all()
    tiposInsumo = TipoInsumo.objects.all()
    tiposOrigen = tipoOrigen.objects.all()

    return render(request, "gestionProductos.html", {
        'productos': productos,
        'semillas': tiposSemillas,
        'insumos': tiposInsumo,
        'origenes': tiposOrigen,"ventas":ventas,"cantidadVentas":cantidadVentas,
        'ventasUsuario': ventasUsuario
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
    filtro = request.GET.get('filtro')  
    productos = Producto.objects.all()  
    ventasPagina = DetalleVenta.objects.all()
    ventas = 0
    for p in ventasPagina:
        ventas += p.cantidad * p.precio
    vendidos = Venta.objects.all()
    cantidadVentas = ventasPagina.count()
   

    if filtro == 'ventas':
        productos = DetalleVenta.objects.all() 
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
            return redirect('adminConfig')
        else:  
            
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

    fecha_subida = request.GET.get('fecha_subida', '-')
    tipo_producto = request.GET.get('tipo', '-')
    ordenar = request.GET.get('ordenar', '-')

    if fecha_subida == 'dia':
        productos = productos.filter(fechasubida=timezone.now().date())
    elif fecha_subida == 'mes':
        productos = productos.filter(fechasubida__month=timezone.now().month)
    elif fecha_subida == 'ano':
        productos = productos.filter(fechasubida__year=timezone.now().year)

    if tipo_producto == 'semilla':
        productos = productos.filter(tipo='semilla')
    elif tipo_producto == 'insumo':
        productos = productos.filter(tipo='insumo')

    if ordenar == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar == 'vendidos_desc':
        productos = productos.order_by('-cantidadVentas')
    elif ordenar == 'vendidos_asc':
        productos = productos.order_by('cantidadVentas')
    tiposSemillas = TipoSemilla.objects.all()
    tiposInsumo = TipoInsumo.objects.all()
    tiposOrigen = tipoOrigen.objects.all()

    
    return render(request, "AdminTemplate.html", {
        'productos': productos,
        'semillas': tiposSemillas,
        'insumos': tiposInsumo,
        'origenes': tiposOrigen,
        'ventas': ventas,
        'cantidadVentas': cantidadVentas
    })


def comprar(request):
    if request.user.is_authenticated:
        carrito = request.session.get("carrito", [])
        total = 0
        for item in carrito:
            total += item["subtotal"]

        venta = Venta()
        usuario = Usuario.objects.get(usuario=request.user) 
        venta.cliente = usuario  
        venta.total = total
        venta.save()
        
        for item in carrito:
            detalle = DetalleVenta()
            detalle.producto = Producto.objects.get(id=item["id"])
            productos = Producto.objects.get(id=item["id"])
            if productos.stock <= 0:
                messages.error(request, 'No hay suficiente stock para realizar la compra')
                return redirect('carrito')
            if item["cantidad"] > productos.stock:
                messages.error(request, 'No hay suficiente stock para realizar la compra')
                return redirect('carrito')
            productos.stock -= item["cantidad"]
            productos.save()
            detalle.precio = item["precio"]
          
            detalle.cantidad = item["cantidad"]
            ventasProductos = DetalleVenta.objects.filter(producto__id=productos.id)
            detalle.producto.cantidadVentas = ventasProductos.count()
            detalle.venta = venta
            productos.save()
            detalle.save()

        del request.session["carrito"]
        messages.success(request, 'Compra realizada correctamente')
        return redirect('carrito')
    else:
        messages.success(request, 'Debe iniciar sesión para comprar productos')
        return redirect("login")
    

def comprarUnProducto(request, id):
    if (request.user.is_authenticated):
        producto = Producto.objects.get(id=id)
        venta = Venta()
        usuario = Usuario.objects.get(usuario=request.user) 
        venta.cliente = usuario
        venta.total = producto.precio
        venta.save()
        detalle = DetalleVenta()
        detalle.producto = producto
        detalle.producto.cantidadVentas += 1
        detalle.precio = producto.precio
        detalle.cantidad = 1
        detalle.venta = venta
        detalle.save()
        if producto.stock <= 1:
            messages.error(request, 'No hay suficiente stock para realizar la compra')
            return redirect('home')
        producto.stock -= 1

        producto.save()
        messages.success(request, 'Compra realizada correctamente')
        return redirect('home')
    else:
        messages.success(request, 'Debe iniciar sesión para comprar productos')
        return redirect("login")



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
    messages.success(request, 'Producto Eliminado del Carrito')
    return render(request, "carro.html")

def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    if (request.path == 'gestion/producto'):
        path = 'GestProducto'
    else:
        path = 'adminConfig'
    return redirect(path) 


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
