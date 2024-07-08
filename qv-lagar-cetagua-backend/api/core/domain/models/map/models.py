from django.db import models
from api.core.domain.models.exploitation.models import Exploitation

class Map(models.Model): 
    """
    Map Model
    This model contains the information of the map in the database
    Attributes: id, name, description, geojson, exploitation
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    geojson = models.JSONField() #mapa de la explotación
    exploitation = models.ForeignKey(Exploitation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ Config Meta class for Map model """
        db_table = 'api_map'
        verbose_name = 'Map'
        verbose_name_plural = 'Maps'

    def __str__(self):
        """ String representation of the map """
        return self.name