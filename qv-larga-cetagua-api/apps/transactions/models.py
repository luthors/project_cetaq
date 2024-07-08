from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Files(models.Model):
    file = models.FileField(upload_to='store/file/')

    class Meta:
        db_table = 'files'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
        
    def __str__(self):
        return str(self.file)
        