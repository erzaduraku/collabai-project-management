from django.contrib import admin

from .models import (
    AIRequest,
    CacheEntity,
)


admin.site.register(AIRequest)
admin.site.register(CacheEntity)
