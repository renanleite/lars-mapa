from django.contrib import admin

# Register your models here.

from django.contrib.gis.admin import OSMGeoAdmin
from .models import *

@admin.register(Local)
class LocalAdmin(OSMGeoAdmin):
    list_display = ('latitude', 'longitude', 'especie', 'owner')
    
@admin.register(Genero)
class GeneroAdmin(OSMGeoAdmin):
    list_display = ('genero',)
    
@admin.register(Especie)
class EspecieAdmin(OSMGeoAdmin):
    list_display = ('especie', 'genero')