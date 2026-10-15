from django.contrib import admin
from .models import Funcionario, Fiscalizacion, Auditoria

admin.site.register(Funcionario)
admin.site.register(Fiscalizacion)
admin.site.register(Auditoria)