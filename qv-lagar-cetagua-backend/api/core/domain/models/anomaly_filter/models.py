from django.db import models
from api.core.domain.models.anomaly_filter.choices import TOLERANCE_TYPE

from api.core.domain.models.sector.models import Sector

# Create your models here.
####### ANOMALIAS FILTERS ########
class AnomalyFilter(models.Model):
    """
    Anomaly Filter Model
    This model contains the information of the anomaly filter in the database
    Attributes: id, number_of_days, tolerance, indicator_number, sector
    """
    id = models.AutoField(primary_key=True)
    number_of_days= models.IntegerField()
    tolerance = models.CharField(max_length=10, choices=TOLERANCE_TYPE, default='MEDIA')
    indicator_number = models.IntegerField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ Meta class for anomaly filter model """
        db_table = 'api_anomaly_filter'
        verbose_name = 'Anomaly Filter'
        verbose_name_plural = 'Anomaly Filters'

    def __str__(self):
        """ String representation of the anomaly filter """
        return str(self.id)
