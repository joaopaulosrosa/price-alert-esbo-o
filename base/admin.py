from django.contrib import admin

# Register your models here.

from .models import AlarmAsset, Asset

admin.site.register(Asset)
admin.site.register(AlarmAsset)
