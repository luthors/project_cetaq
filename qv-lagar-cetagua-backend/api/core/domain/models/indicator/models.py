from django.db import models

# Create your models here.
class Indicator(models.Model):
    """
    Indicator Model
    This model contains the information of the indicator in the database
    Attributes: id, name, description
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta class for indicator model"""
        db_table = 'api_indicator'
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'

    def __str__(self):
        """String representation of the indicator"""
        return self.name