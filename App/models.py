from django.db import models


class Funcionario(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    identificador = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Fiscalizacion(models.Model):
    patente = models.CharField(max_length=10)
    tipo_vehiculo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    fotografia = models.ImageField(upload_to='fiscalizaciones/')
    observaciones = models.TextField(blank=True)

    estado = models.CharField(
        max_length=30,
        default='Pendiente'
    )

    resultado = models.CharField(
        max_length=50,
        blank=True
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.patente


class Auditoria(models.Model):
    usuario = models.CharField(max_length=100)
    accion = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    fiscalizacion = models.ForeignKey(
        Fiscalizacion,
        on_delete=models.CASCADE
    )

    descripcion = models.TextField()

    def __str__(self):
        return self.accion