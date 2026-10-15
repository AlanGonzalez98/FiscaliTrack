
import re

from django.utils import timezone
from rest_framework import serializers

from .models import Funcionario, Fiscalizacion, Auditoria


class FuncionarioSerializer(serializers.ModelSerializer):

    def validate_nombre(self, value):
        if any(caracter.isdigit() for caracter in value):
            raise serializers.ValidationError(
                "El nombre no puede contener números."
            )
        return value.strip()

    class Meta:
        model = Funcionario
        fields = '__all__'


class FiscalizacionSerializer(serializers.ModelSerializer):

    def validate_patente(self, value):
        patente = re.sub(r'[\s.-]', '', value).upper()

        patron_antiguo = r'^[A-Z]{2}[0-9]{4}$'
        patron_actual = r'^[BCDFGHJKLPRSTVWXYZ]{4}[0-9]{2}$'

        if not (
            re.fullmatch(patron_antiguo, patente)
            or re.fullmatch(patron_actual, patente)
        ):
            raise serializers.ValidationError(
                'Ingrese una patente chilena válida. '
                'Ejemplos: AB1234 o BCDF12.'
            )

        return patente

    def validate(self, attrs):
        funcionario = attrs.get(
            'funcionario',
            getattr(self.instance, 'funcionario', None)
        )

        if funcionario is not None and not funcionario.activo:
            raise serializers.ValidationError({
                'funcionario': (
                    'No se puede asignar un funcionario inactivo.'
                )
            })

        patente = attrs.get(
            'patente',
            getattr(self.instance, 'patente', None)
        )

        fecha_hora = attrs.get(
            'fecha_hora',
            getattr(self.instance, 'fecha_hora', None)
        )

        if patente and fecha_hora:
            fecha_local = timezone.localtime(fecha_hora).date()

            duplicada = Fiscalizacion.objects.filter(
                patente=patente,
                fecha_hora__date=fecha_local
            )

            if self.instance:
                duplicada = duplicada.exclude(
                    pk=self.instance.pk
                )

            if duplicada.exists():
                raise serializers.ValidationError({
                    'patente': (
                        'Este vehículo ya fue fiscalizado durante '
                        'ese día. Podrá fiscalizarse nuevamente '
                        'desde las 00:00 del día siguiente.'
                    )
                })

        return attrs

    class Meta:
        model = Fiscalizacion
        fields = '__all__'


class AuditoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auditoria
        fields = '__all__'
        read_only_fields = ['fecha_hora']
