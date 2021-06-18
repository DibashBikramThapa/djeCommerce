from django.contrib import admin
from eCom import models

# Register your models here.
admin.site.register(models.Order)
admin.site.register(models.Item)
admin.site.register(models.OrderItem)
