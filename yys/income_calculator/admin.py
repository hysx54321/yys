from django.contrib import admin

# Register your models here.
from .models import (
    Item,
    Period,
    Event,
    EventGroup,
    EventEntity,
)

admin.site.register(Item)
admin.site.register(Period)
admin.site.register(Event)
admin.site.register(EventGroup)
admin.site.register(EventEntity)
