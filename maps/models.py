from django.db import models
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

# from django.contrib.gis.db import models

class Genero(models.Model):
   
    genero = models.CharField(max_length=80)
    
    def __str__(self) -> str:
        return self.genero
    
class Especie(models.Model):
   
    especie = models.CharField(max_length=80)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.especie

class Local(models.Model):
    # location = models.PointField(geography=True, default=Point(-13.0, -50.0))
    
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
    )
    especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

