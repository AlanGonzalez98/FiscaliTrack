from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from App import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # Autenticación JWT
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Página web
    path('', views.vista_principal, name='inicio'),
    path('fiscalizacion/', views.vista_fiscalizacion, name='fiscalizacion'),
    path('fiscalizacion/editar/<int:id>/', views.editar_fiscalizacion, name='editar_fiscalizacion'),
    path('fiscalizacion/eliminar/<int:id>/', views.eliminar_fiscalizacion, name='eliminar_fiscalizacion'),

    # Auditorías
    path('auditoria/', views.vista_auditoria, name='auditoria'),
    path('auditoria/editar/<int:id>/', views.editar_auditoria, name='editar_auditoria'),
    path('auditoria/eliminar/<int:id>/', views.eliminar_auditoria, name='eliminar_auditoria'),

    # Funcionarios
    path('funcionarios/', views.vista_funcionarios, name='funcionarios'),
    path(
        'funcionarios/estado/<int:pk>/',
        views.cambiar_estado_funcionario,
        name='cambiar_estado_funcionario'
    ),

    # API de funcionarios
    path('api/funcionarios/', views.FuncionarioListaCrearAPI.as_view(), name='api_funcionarios'),
    path('api/funcionarios/<int:pk>/', views.FuncionarioDetalleAPI.as_view(), name='api_funcionario_detalle'),

    # API de fiscalizaciones
    path('api/fiscalizaciones/', views.FiscalizacionListaCrearAPI.as_view(), name='api_fiscalizaciones'),
    path('api/fiscalizaciones/<int:pk>/', views.FiscalizacionDetalleAPI.as_view(), name='api_fiscalizacion_detalle'),

    # API de auditorías
    path('api/auditorias/', views.AuditoriaListaCrearAPI.as_view(), name='api_auditorias'),
    path('api/auditorias/<int:pk>/', views.AuditoriaDetalleAPI.as_view(), name='api_auditoria_detalle'),
]

# Archivos multimedia
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)