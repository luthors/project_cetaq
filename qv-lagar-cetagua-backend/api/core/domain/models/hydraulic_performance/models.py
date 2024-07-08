from django.db import models
from api.core.domain.models.sector.models import Sector

class HydraulicPerformance(models.Model):
    """
    Hydraulic Performance Model
    This model contains the information of the hydraulic performance in the database
    Attributes: id, sector, year, bimester, hp_total_percentage
    """
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    year = models.IntegerField()
    bimester = models.IntegerField()
    hp_total_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ Meta class for hydraulic performance model """
        db_table = 'api_hydraulic_performance'
        verbose_name = 'Hydraulic Performance'
        verbose_name_plural = 'Hydraulic Performances'

    def __str__(self):
        """ String representation of the hydraulic performance """
        return str(self.id)
