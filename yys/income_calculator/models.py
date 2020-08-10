from django.db import models


# Create your models here.
class BasicModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)  # a short description of the object
    comment = models.TextField()
    time_created = models.PositiveIntegerField()
    time_modified = models.PositiveIntegerField()
    deleted = models.BooleanField()

    def __str__(self):
        """String for representing the Model object."""
        return self.description


class Event(BasicModel):
    display_name = models.CharField(max_length=20)
    min = models.IntegerField()
    max = models.IntegerField()
    expectation_value = models.IntegerField()
    default_frequency = models.IntegerField()
    default_total = models.IntegerField()
    priority = models.SmallIntegerField()
    period_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField()
    icon = models.TextField()


class Item(BasicModel):
    pass


class Period(BasicModel):
    num_days = models.PositiveIntegerField()


