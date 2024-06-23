from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SmileCenter
from .models import CenterType
from .models import SmileCenterByCenterType
from .models import Service
from .models import SmileCenterByServices
from .models import Zone
from .models import SmileCenterByZones

#add models to view in Admin
admin.site.register(SmileCenter)
admin.site.register(CenterType)
admin.site.register(SmileCenterByCenterType)
admin.site.register(Service)
admin.site.register(SmileCenterByServices)
admin.site.register(Zone)
admin.site.register(SmileCenterByZones)
