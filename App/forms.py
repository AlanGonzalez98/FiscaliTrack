from django import forms

from .models import Fiscalizacion
from .models import Funcionario
from .models import Auditoria

import re


class FiscalizacionForm(forms.ModelForm):

    class Meta:

        model = Fiscalizacion

        fields = [
            'patente',
            'tipo_vehiculo',
            'marca',
            'modelo',
            'color',
            'fecha_hora',
            'motivo',
            'fotografia',
            'observaciones',
            'estado',
            'resultado',
            'funcionario'
        ]

        widgets = {

            'patente': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),

            'tipo_vehiculo': forms.Select(
                choices=[
                    ('', 'Seleccione un tipo de vehículo'),
                    ('Sedán', 'Sedán'),
                    ('SUV', 'SUV'),
                    ('SUV compacta', 'SUV compacta'),
                    ('Hatchback', 'Hatchback'),
                    ('Pickup', 'Pickup'),
                    ('Station Wagon', 'Station Wagon'),
                    ('Van', 'Van'),
                    ('Furgón', 'Furgón'),
                    ('Camión', 'Camión'),
                    ('Bus', 'Bus'),
                    ('Motocicleta', 'Motocicleta'),
                    ('Otro', 'Otro')
                ],
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            ),

            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),

            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),

            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),

            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'required': True
                }
            ),

            'motivo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),

            'fotografia': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),

            'estado': forms.Select(
                choices=[
                    ('Pendiente', 'Pendiente'),
                    ('En proceso', 'En proceso'),
                    ('Completada', 'Completada'),
                    ('Cancelada', 'Cancelada')
                ],
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            ),

            'resultado': forms.Select(
                choices=[
                    ('', 'Seleccione un resultado'),
                    ('Fiscalización realizada', 'Fiscalización realizada'),
                    ('Sin infracciones', 'Sin infracciones'),
                    ('Con infracción', 'Con infracción'),
                    ('Vehículo se dio a la fuga', 'Vehículo se dio a la fuga'),
                    ('Fiscalización no realizada', 'Fiscalización no realizada')
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'funcionario': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            )
        }


    def clean_patente(self):

        patente = self.cleaned_data['patente']

        patente = patente.upper().replace(' ', '')

        patron = r'^[A-Z]{2}[0-9]{4}$|^[A-Z]{4}[0-9]{2}$'

        if not re.match(
            patron,
            patente
        ):

            raise forms.ValidationError(
                'La patente debe tener un formato válido. Ejemplo: AB1234 o ABCD12.'
            )

        return patente


    def clean_tipo_vehiculo(self):

        tipo = self.cleaned_data['tipo_vehiculo']

        if not tipo:

            raise forms.ValidationError(
                'Debe seleccionar el tipo de vehículo.'
            )

        return tipo


    def clean_marca(self):

        marca = self.cleaned_data['marca'].strip()

        if not marca:

            raise forms.ValidationError(
                'Debe ingresar la marca.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\-]+$',
            marca
        ):

            raise forms.ValidationError(
                'La marca solo puede contener letras.'
            )

        return marca


    def clean_modelo(self):

        modelo = self.cleaned_data['modelo'].strip()

        if not modelo:

            raise forms.ValidationError(
                'Debe ingresar el modelo.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s\-]+$',
            modelo
        ):

            raise forms.ValidationError(
                'El modelo contiene caracteres no permitidos.'
            )

        return modelo


    def clean_color(self):

        color = self.cleaned_data['color'].strip()

        if not color:

            raise forms.ValidationError(
                'Debe ingresar el color.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
            color
        ):

            raise forms.ValidationError(
                'El color solo puede contener letras.'
            )

        return color


    def clean_motivo(self):

        motivo = self.cleaned_data['motivo'].strip()

        if not motivo:

            raise forms.ValidationError(
                'Debe ingresar el motivo de la fiscalización.'
            )

        if len(motivo) < 5:

            raise forms.ValidationError(
                'El motivo debe tener al menos 5 caracteres.'
            )

        return motivo


    def clean_observaciones(self):

        observaciones = self.cleaned_data.get(
            'observaciones',
            ''
        ).strip()

        if observaciones:

            if len(observaciones) < 3:

                raise forms.ValidationError(
                    'La observación debe tener al menos 3 caracteres.'
                )

        return observaciones


class FuncionarioForm(forms.ModelForm):

    class Meta:

        model = Funcionario

        fields = [
            'nombre',
            'cargo',
            'identificador',
            'activo'
        ]


    def clean_nombre(self):

        nombre = self.cleaned_data['nombre'].strip()

        if not nombre:

            raise forms.ValidationError(
                'Debe ingresar el nombre.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
            nombre
        ):

            raise forms.ValidationError(
                'El nombre solo puede contener letras.'
            )

        return nombre


    def clean_cargo(self):

        cargo = self.cleaned_data['cargo'].strip()

        if not cargo:

            raise forms.ValidationError(
                'Debe ingresar el cargo.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
            cargo
        ):

            raise forms.ValidationError(
                'El cargo solo puede contener letras.'
            )

        return cargo


    def clean_identificador(self):

        identificador = self.cleaned_data['identificador'].strip()

        if not identificador:

            raise forms.ValidationError(
                'Debe ingresar el identificador.'
            )

        if not re.match(
            r'^[0-9]+$',
            identificador
        ):

            raise forms.ValidationError(
                'El identificador solo puede contener números.'
            )

        return identificador


class AuditoriaForm(forms.ModelForm):

    class Meta:

        model = Auditoria

        fields = [
            'usuario',
            'accion',
            'descripcion',
            'fiscalizacion'
        ]


    def clean_usuario(self):

        usuario = self.cleaned_data['usuario'].strip()

        if not usuario:

            raise forms.ValidationError(
                'Debe ingresar el usuario.'
            )

        if not re.match(
            r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
            usuario
        ):

            raise forms.ValidationError(
                'El usuario solo puede contener letras.'
            )

        return usuario


    def clean_accion(self):

        accion = self.cleaned_data['accion'].strip()

        if not accion:

            raise forms.ValidationError(
                'Debe ingresar la acción.'
            )

        return accion


    def clean_descripcion(self):

        descripcion = self.cleaned_data['descripcion'].strip()

        if not descripcion:

            raise forms.ValidationError(
                'Debe ingresar una descripción.'
            )

        if len(descripcion) < 5:

            raise forms.ValidationError(
                'La descripción debe tener al menos 5 caracteres.'
            )

        return descripcion