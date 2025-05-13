from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.exceptions import PermissionDenied
from .models import Link, Articulo, EstadoClasificacion, Rol, Profile
from .forms import LinkForm, ClasificacionForm, ArticuloForm

# === Decoradores de autorización por rol ===
def solo_prensa(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.rol not in [Rol.PRENSA, Rol.ADMIN]:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def solo_clasificacion(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.rol not in [Rol.CLASIFICACION, Rol.ADMIN]:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def solo_redaccion(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.rol not in [Rol.REDACCION, Rol.ADMIN]:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def solo_publicacion(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.rol not in [Rol.PUBLICACION, Rol.ADMIN]:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# === Dashboard por rol ===
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    rol = request.user.profile.rol
    if rol == Rol.PRENSA:
        return redirect('cargar_link')
    elif rol == Rol.CLASIFICACION:
        return redirect('listar_links_pendientes')
    elif rol == Rol.REDACCION:
        return redirect('crear_articulo')
    elif rol == Rol.PUBLICACION:
        return redirect('lista_articulos')
    elif rol == Rol.ADMIN:
        return redirect('dashboard_admin')
    return redirect('lista_articulos')

# === Vistas de Prensa ===
@solo_prensa
def cargar_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.cargado_por = request.user
            link.save()
            form.save_m2m()
            return redirect('lista_links')
    else:
        form = LinkForm()
    return render(request, 'links/cargar_link.html', {'form': form})

# === Vistas de Clasificación ===
@solo_clasificacion
def listar_links_pendientes(request):
    links = Link.objects.filter(estado_clasificacion=EstadoClasificacion.PENDIENTE)
    return render(request, 'clasificacion/lista_links_pendientes.html', {'links': links})

@solo_clasificacion
def clasificar_link(request, link_id):
    link = get_object_or_404(Link, pk=link_id)
    if request.method == 'POST':
        form = ClasificacionForm(request.POST, instance=link)
        if form.is_valid():
            link = form.save(commit=False)
            link.fecha_aprobacion = now()
            link.clasificado_por = request.user
            link.save()
            return redirect('listar_links_pendientes')
    else:
        form = ClasificacionForm(instance=link)
    return render(request, 'clasificacion/clasificar_link.html', {'form': form, 'link': link})

# === Vistas de Redacción ===
@solo_redaccion
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.redactado_por = request.user
            articulo.save()
            form.save_m2m()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'articulos/crear_articulo.html', {'form': form})

# === Listado y detalle de artículos ===
def lista_articulos(request):
    articulos = Articulo.objects.all().order_by('-fecha_redaccion')
    return render(request, 'articulos/lista_articulos.html', {'articulos': articulos})

def ver_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    puede_exportar = request.user.is_authenticated and request.user.profile.rol in [Rol.PUBLICACION, Rol.ADMIN]
    return render(request, 'articulos/ver_articulo.html', {'articulo': articulo, 'puede_exportar': puede_exportar})

# === Exportación PDF (solo publicación) ===
from django.template.loader import render_to_string
from weasyprint import HTML

@solo_publicacion
def exportar_articulo_pdf(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    html_string = render_to_string("reportes/articulo_pdf.html", {'articulo': articulo})
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="articulo_{articulo.id}.pdf"'
    return response

# === Dashboard admin ===
def dashboard_admin(request):
    if not request.user.is_authenticated or request.user.profile.rol != Rol.ADMIN:
        return redirect('login')

    total_links = Link.objects.count()
    links_pendientes = Link.objects.filter(estado_clasificacion=EstadoClasificacion.PENDIENTE).count()
    links_aprobados = Link.objects.filter(estado_clasificacion=EstadoClasificacion.APROBADO).count()
    links_descartados = Link.objects.filter(estado_clasificacion=EstadoClasificacion.DESCARTADO).count()
    total_articulos = Articulo.objects.count()
    usuarios_por_rol = {
        rol_label: Profile.objects.filter(rol=rol_key).count()
        for rol_key, rol_label in Rol.choices
    }
    articulos_recientes = Articulo.objects.order_by('-fecha_redaccion')[:5]
    links_recientes = Link.objects.order_by('-fecha_carga')[:5]

    return render(request, 'admin/dashboard_admin.html', {
        'total_links': total_links,
        'links_pendientes': links_pendientes,
        'links_aprobados': links_aprobados,
        'links_descartados': links_descartados,
        'total_articulos': total_articulos,
        'usuarios_por_rol': usuarios_por_rol,
        'articulos_recientes': articulos_recientes,
        'links_recientes': links_recientes
    })
