from django.db import models
from api.core.domain.models.exploitation.models import Exploitation
from api.core.domain.models.map.models import Map

class Sector(models.Model):
    """
    Sector Model
    This model contains the information of the sector in the database
    Attributes: id, name, description, map
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    map = models.ForeignKey(Map, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ Config Meta class for Sector model """
        db_table = 'api_sector'
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

    def __str__(self):
        """ String representation of the sector """
        return self.name