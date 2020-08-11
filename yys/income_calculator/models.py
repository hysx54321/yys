from django.db import models
from datetime import datetime

# Create your models here.
class BasicModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)  # a short description of the object
    comment = models.TextField(null=True)
    time_created = models.PositiveIntegerField()
    time_modified = models.PositiveIntegerField()
    deleted = models.BooleanField()

    def __str__(self):
        """String for representing the Model object."""
        return self.description

    @property
    def time_created_string(self):
        return datetime.fromtimestamp(self.time_created)

    @property
    def time_modified_string(self):
        return datetime.fromtimestamp(self.time_modified)


class Event(BasicModel):
    display_name = models.CharField(max_length=20)
    priority = models.SmallIntegerField()
    default_frequency = models.IntegerField()
    icon = models.TextField(null=True)
    period_id = models.PositiveIntegerField()
    event_group_id = models.PositiveIntegerField(null=True)


class EventGroup(BasicModel):
    pass


class EventEntity(BasicModel):
    event_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    expectation_value = models.IntegerField()
    default_total = models.IntegerField()


class Item(BasicModel):
    pass


class Period(BasicModel):
    num_days = models.PositiveIntegerField()


