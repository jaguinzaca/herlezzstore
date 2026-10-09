# HERLEZZ Store

Catálogo de productos en Django con SQLite, administración manual y pedidos por WhatsApp. La página muestra los productos activos de la base de datos; las imágenes subidas desde el administrador se guardan en `media/products/`.

## Inicio rápido (PowerShell, Python 3.12 o superior)

Desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py ensure_dev_admin
python manage.py runserver
```

Catálogo: <http://127.0.0.1:8000/>  
Administrador: <http://127.0.0.1:8000/admin/>

`seed_data` carga seis productos y sus beneficios. Copia los cuatro artes disponibles desde `productosimagenes/` a `media/products/`; los dos combos muestran una ilustración en código hasta que se carguen sus fotos oficiales desde Admin. Puede repetirse sin duplicar productos ni beneficios. También acepta `--source-dir RUTA` si las imágenes originales están en otra carpeta. `seed_products` sigue disponible como alias.

`ensure_dev_admin` crea una sola vez el usuario local `admin` con correo `admin@herlezz.com` y contraseña `admin12345`. El comando solo funciona con `DJANGO_DEBUG=True` y no cambia la contraseña si el usuario ya existe.

## Estructura

- `config/`: configuración de Django, SQLite, rutas, archivos estáticos y archivos subidos.
- `products/models.py`: productos, beneficios técnicos y enlace de pedido personalizado.
- `products/admin.py`: edición, búsqueda, filtros e inserción de beneficios por producto.
- `products/views.py`: catálogo de productos activos.
- `templates/products/catalog.html`: plantilla que Django procesa para el catálogo, con Tailwind CSS CDN.
- El logotipo del navbar se construye con HTML y Tailwind, sin depender de imágenes.
- `products/management/commands/seed_data.py`: carga inicial de seis artículos y sus beneficios.
- `products/management/commands/ensure_dev_admin.py`: alta no interactiva del administrador local.

## Añadir productos

En `/admin/`, abre **Productos**, crea un producto con nombre, slug único, descripción y precio, y marca **Activo** para publicarlo. La imagen es opcional mientras se prepara el arte oficial. En el mismo formulario puedes editar los beneficios y su orden. Puedes desactivar un producto sin borrarlo. El botón de pedido usa el nombre y precio guardados en la base de datos.

## Nota de despliegue

La configuración incluida es para desarrollo local. Antes de publicar, configura `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` y un servicio para archivos estáticos y subidos. La base SQLite y `media/` permanecen locales por defecto.
