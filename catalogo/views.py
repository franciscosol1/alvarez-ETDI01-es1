import json
from pathlib import Path

from django.http import Http404
from django.shortcuts import render


DATOS_PATH = Path(__file__).parent / 'data' / 'productos.json'


def cargar_productos():
    with DATOS_PATH.open(encoding='utf-8') as archivo:
        return json.load(archivo)


def lista_productos(request):
    productos = cargar_productos()
    contexto = {
        'productos': productos,
        'total_productos': len(productos),
        'productos_con_stock': sum(producto['stock'] > 0 for producto in productos),
    }
    return render(request, 'catalogo/lista.html', contexto)


def detalle_producto(request, producto_id):
    producto = next(
        (producto for producto in cargar_productos() if producto['id'] == producto_id),
        None,
    )
    if producto is None:
        raise Http404('El producto no existe.')
    return render(request, 'catalogo/detalle.html', {'producto': producto})