from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Persona

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre','cargo','departamento', 'puesto', 'activo')
    search_fields = ('nomnbre', 'cargo')