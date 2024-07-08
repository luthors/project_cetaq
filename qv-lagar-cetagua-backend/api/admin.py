from django.contrib import admin
from api.core.domain.models.anomaly_filter.models import AnomalyFilter

from api.core.domain.models.exploitation.models import Exploitation
from api.core.domain.models.indicator.models import Indicator
from api.core.domain.models.indicator_threshold.models import IndicatorThreshold
from api.core.domain.models.map.models import Map
from api.core.domain.models.sector.models import Sector





# Register your models here.
admin.site.register(Exploitation)
admin.site.register(Sector)
admin.site.register(IndicatorThreshold)
admin.site.register(Indicator)
admin.site.register(AnomalyFilter)
admin.site.register(Map)
