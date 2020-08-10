from django.contrib import admin

# Register your models here.
from .models import (
    Item,
    Period,
    Event,
)

admin.site.register(Item)
admin.site.register(Period)
admin.site.register(Event)
