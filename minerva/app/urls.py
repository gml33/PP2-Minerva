from django.urls import path
from . import views

urlpatterns = [
    # Dashboard general
    path('', views.dashboard, name='dashboard'),

    # Prensa
    path('links/nuevo/', views.cargar_link, name='cargar_link'),

    # Clasificación
    path('clasificacion/', views.listar_links_pendientes, name='listar_links_pendientes'),
    path('clasificacion/<int:link_id>/', views.clasificar_link, name='clasificar_link'),

    # Redacción
    path('articulos/nuevo/', views.crear_articulo, name='crear_articulo'),

    # Artículos
    path('articulos/', views.lista_articulos, name='lista_articulos'),
    path('articulo/<int:articulo_id>/', views.ver_articulo, name='ver_articulo'),
    path('articulo/<int:articulo_id>/exportar/', views.exportar_articulo_pdf, name='exportar_articulo_pdf'),

    # Dashboard Admin
    path('admin/dashboard/', views.dashboard_admin, name='dashboard_admin'),
]
