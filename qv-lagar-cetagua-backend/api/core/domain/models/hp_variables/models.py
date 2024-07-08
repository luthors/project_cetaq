from django.db import models
from api.core.domain.models.hydraulic_performance.models import HydraulicPerformance

class HPVariables(models.Model):
    """
    HP Variables Model
    This model contains the information of the variables in the database
    Attributes: id, hydraulic_performance, contract_number, liters_supplied, percentage_adjustment, percentage_telereading
    """
    id = models.AutoField(primary_key=True)
    hydraulic_performance = models.OneToOneField(HydraulicPerformance, on_delete=models.CASCADE)
    contract_number = models.IntegerField()
    liters_supplied = models.FloatField()
    percentage_adjustment = models.FloatField()
    percentage_telereading = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ Meta class for hp variables model """
        db_table = 'api_hp_variables'
        verbose_name = 'HP Variables'
        verbose_name_plural = 'HP Variables'

    def __str__(self):
        """ String representation of the hp variables """
        return str(self.id)