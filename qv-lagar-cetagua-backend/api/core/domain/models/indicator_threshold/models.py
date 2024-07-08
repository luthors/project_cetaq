from django.db import models
from api.core.domain.models.anomaly_filter.models import AnomalyFilter
from api.core.domain.models.indicator.models import Indicator

class IndicatorThreshold(models.Model):
    """
    Indicator Threshold Model
    This model contains the information of the indicator threshold in the database
    Attributes: id, active, meanWeekDays, meanSurrounding, hours, tolerance, 
    movingAverageDays, fixedAverageDays, weightAverage, weightDeviation, anomaly_filter, indicator
    """
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(null=True)
    meanWeekDays = models.IntegerField(null=True)
    meanSurrounding = models.FloatField(null=True)
    hours = models.IntegerField(null=True)
    tolerance = models.FloatField(null=True)
    movingAverageDays = models.IntegerField(null=True)
    fixedAverageDays = models.IntegerField(null=True)    
    weightAverage = models.FloatField(null=True)
    weightDeviation = models.FloatField(null=True)
    anomaly_filter = models.ForeignKey(AnomalyFilter, on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """ Meta class for indicator threshold model """
        db_table = 'api_indicator_threshold'
        verbose_name = 'Indicator Threshold'
        verbose_name_plural = 'Indicator Thresholds'

    def __str__(self):
        """ String representation of the indicator threshold """
        return str(self.id)