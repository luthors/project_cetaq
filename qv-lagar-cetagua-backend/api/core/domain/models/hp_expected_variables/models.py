from django.db import models
from api.core.domain.models.hydraulic_performance.models import HydraulicPerformance

class HPExpectedVariables(models.Model):
    """ 
    HP Expected Variables Model
    This model contains the information of the expected variables in the database
    Attributes: id, hydraulic_performance, hp_expected, supplied_expected, registed_expected
    """
    id = models.AutoField(primary_key=True)
    hydraulic_performance = models.OneToOneField(HydraulicPerformance, on_delete=models.CASCADE)
    hp_expected = models.FloatField()
    supplied_expected = models.FloatField()
    registed_expected = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ Meta class for hp expected variables model """
        db_table = 'api_hp_expected_variables'
        verbose_name = 'HP Expected Variables'
        verbose_name_plural = 'HP Expected Variables'

    def __str__(self):
        """ String representation of the hp expected variables """
        return str(self.id)
