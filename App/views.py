
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Fiscalizacion, Funcionario, Auditoria

from .forms import FiscalizacionForm
from .forms import FuncionarioForm
from .forms import AuditoriaForm

import re

# Imports para la API REST
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import (
    FuncionarioSerializer,
    FiscalizacionSerializer,
    AuditoriaSerializer,
)





# =====================================
# VALIDACIÓN DE PATENTES CHILENAS
# =====================================

def normalizar_patente(patente):
    """
    Convierte la patente a mayúsculas y elimina
    espacios, puntos y guiones.
    Ejemplo: bc-df.12 -> BCDF12
    """
    return re.sub(r'[\s.-]', '', patente).upper()


def patente_valida(patente):
    """
    Formatos para vehículos de cuatro o más ruedas:

    Antiguo: AB1234
    Actual:  BCDF12

    El formato actual utiliza las letras permitidas
    para las patentes chilenas.
    """
    patron_antiguo = r'^[A-Z]{2}[0-9]{4}$'
    patron_actual = r'^[BCDFGHJKLPRSTVWXYZ]{4}[0-9]{2}$'

    return (
        re.fullmatch(patron_antiguo, patente) is not None
        or re.fullmatch(patron_actual, patente) is not None
    )


def vista_principal(request):
    return render(
        request,
        'index.html'
    )


def vista_fiscalizacion(request):

    funcionarios = Funcionario.objects.filter(
        activo=True
    )

    patente_buscada = normalizar_patente(
        request.GET.get('buscar_patente', '')
    )

    fiscalizacion_encontrada = None

    # BUSCADOR DE PATENTES

    if patente_buscada:

        if not patente_valida(patente_buscada):

            messages.error(
                request,
                'Ingrese una patente chilena válida. '
                'Ejemplos: AB1234 o BCDF12.'
            )

            patente_buscada = ''

        else:

            ahora = timezone.localtime()

            inicio_dia = ahora.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )

            fin_dia = inicio_dia + timedelta(days=1)

            fiscalizacion_encontrada = Fiscalizacion.objects.filter(
                patente=patente_buscada,
                fecha_hora__gte=inicio_dia,
                fecha_hora__lt=fin_dia
            ).order_by(
                '-fecha_hora'
            ).first()

    # CREAR FISCALIZACIÓN

    if request.method == 'POST':

        datos = request.POST.copy()

        if 'patente' in datos:
            datos['patente'] = normalizar_patente(
                datos['patente']
            )

        form = FiscalizacionForm(
            datos,
            request.FILES
        )

        if form.is_valid():

            patente = normalizar_patente(
                form.cleaned_data['patente']
            )

            if not patente_valida(patente):

                messages.error(
                    request,
                    'La patente ingresada no corresponde '
                    'a un formato válido de patente chilena.'
                )

                fiscalizaciones = Fiscalizacion.objects.all().order_by(
                    '-fecha_hora'
                )

                return render(
                    request,
                    'fiscalizacion.html',
                    {
                        'form': form,
                        'funcionarios': funcionarios,
                        'fiscalizaciones': fiscalizaciones,
                        'patente_buscada': patente_buscada,
                        'fiscalizacion_encontrada': fiscalizacion_encontrada
                    }
                )

            form.instance.patente = patente

            ahora = timezone.localtime()

            inicio_dia = ahora.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )

            fin_dia = inicio_dia + timedelta(days=1)

            ya_fiscalizado = Fiscalizacion.objects.filter(
                patente=patente,
                fecha_hora__gte=inicio_dia,
                fecha_hora__lt=fin_dia
            ).exists()

            if ya_fiscalizado:

                messages.warning(
                    request,
                    'Este vehículo ya fue fiscalizado durante '
                    'el día de hoy. Podrá fiscalizarse nuevamente '
                    'desde las 00:00 del día siguiente.'
                )

                return redirect(
                    '/fiscalizacion/'
                )

            fiscalizacion = form.save()

            funcionario = fiscalizacion.funcionario

            Auditoria.objects.create(
                usuario=funcionario.nombre,
                accion='CREAR',
                fiscalizacion=fiscalizacion,
                descripcion='Se registró una nueva fiscalización.'
            )

            messages.success(
                request,
                'Fiscalización registrada correctamente.'
            )

            return redirect(
                '/fiscalizacion/'
            )

        else:

            messages.error(
                request,
                'Existen errores en el formulario. Revise los datos ingresados.'
            )

    else:

        form = FiscalizacionForm()

    fiscalizaciones = Fiscalizacion.objects.all().order_by(
        '-fecha_hora'
    )

    return render(
        request,
        'fiscalizacion.html',
        {
            'form': form,
            'funcionarios': funcionarios,
            'fiscalizaciones': fiscalizaciones,
            'patente_buscada': patente_buscada,
            'fiscalizacion_encontrada': fiscalizacion_encontrada
        }
    )


def editar_fiscalizacion(request, id):

    fiscalizacion = Fiscalizacion.objects.get(
        id=id
    )

    funcionarios = Funcionario.objects.filter(
        activo=True
    )

    if request.method == 'POST':

        datos = request.POST.copy()

        if 'patente' in datos:
            datos['patente'] = normalizar_patente(
                datos['patente']
            )

        form = FiscalizacionForm(
            datos,
            request.FILES,
            instance=fiscalizacion
        )

        if form.is_valid():

            patente = normalizar_patente(
                form.cleaned_data['patente']
            )

            if not patente_valida(patente):

                messages.error(
                    request,
                    'La patente ingresada no corresponde '
                    'a un formato válido de patente chilena.'
                )

            else:

                form.instance.patente = patente
                form.save()

                funcionario = fiscalizacion.funcionario

                Auditoria.objects.create(
                    usuario=funcionario.nombre,
                    accion='EDITAR',
                    fiscalizacion=fiscalizacion,
                    descripcion='Se modificó una fiscalización.'
                )

                messages.success(
                    request,
                    'Fiscalización modificada correctamente.'
                )

                return redirect(
                    '/fiscalizacion/'
                )

        else:

            messages.error(
                request,
                'Existen errores en el formulario. Revise los datos ingresados.'
            )

    else:

        form = FiscalizacionForm(
            instance=fiscalizacion
        )

    return render(
        request,
        'editar_fiscalizacion.html',
        {
            'form': form,
            'fiscalizacion': fiscalizacion,
            'funcionarios': funcionarios
        }
    )


def eliminar_fiscalizacion(request, id):

    fiscalizacion = Fiscalizacion.objects.get(
        id=id
    )

    fiscalizacion.delete()

    messages.success(
        request,
        'Fiscalización eliminada correctamente.'
    )

    return redirect(
        '/fiscalizacion/'
    )


def vista_funcionarios(request):

    if request.method == 'POST':

        form = FuncionarioForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Funcionario registrado correctamente.'
            )

            return redirect(
                '/funcionarios/'
            )

        else:

            messages.error(
                request,
                'Existen errores en el formulario.'
            )

    else:

        form = FuncionarioForm()

    funcionarios = Funcionario.objects.all().order_by(
        'nombre'
    )

    return render(
        request,
        'funcionarios.html',
        {
            'form': form,
            'funcionarios': funcionarios
        }
    )


def vista_auditoria(request):

    auditorias = Auditoria.objects.all().order_by(
        '-fecha_hora'
    )

    return render(
        request,
        'auditoria.html',
        {
            'auditorias': auditorias
        }
    )


def editar_auditoria(request, id):

    auditoria = Auditoria.objects.get(
        id=id
    )

    if request.method == 'POST':

        form = AuditoriaForm(
            request.POST,
            instance=auditoria
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Auditoría modificada correctamente.'
            )

            return redirect(
                '/auditoria/'
            )

        else:

            messages.error(
                request,
                'Existen errores en el formulario.'
            )

    else:

        form = AuditoriaForm(
            instance=auditoria
        )

    return render(
        request,
        'editar_auditoria.html',
        {
            'form': form,
            'auditoria': auditoria
        }
    )


def eliminar_auditoria(request, id):

    auditoria = Auditoria.objects.get(
        id=id
    )

    auditoria.delete()

    messages.success(
        request,
        'Auditoría eliminada correctamente.'
    )

    return redirect(
        '/auditoria/'
    )


# =====================================
# VISTAS DE LA API REST
# =====================================

class FuncionarioListaCrearAPI(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all().order_by('nombre')
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]


class FuncionarioDetalleAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]


class FiscalizacionListaCrearAPI(generics.ListCreateAPIView):
    queryset = Fiscalizacion.objects.all().order_by('-fecha_hora')
    serializer_class = FiscalizacionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class FiscalizacionDetalleAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fiscalizacion.objects.all()
    serializer_class = FiscalizacionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class AuditoriaListaCrearAPI(generics.ListCreateAPIView):
    queryset = Auditoria.objects.all().order_by('-fecha_hora')
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated]


class AuditoriaDetalleAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated]





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Funcionario


@require_POST
def cambiar_estado_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    funcionario.activo = not funcionario.activo
    funcionario.save(update_fields=['activo'])

    if funcionario.activo:
        messages.success(
            request,
            f'El funcionario {funcionario.nombre} fue activado.'
        )
    else:
        messages.success(
            request,
            f'El funcionario {funcionario.nombre} fue desactivado.'
        )

    return redirect('funcionarios')
