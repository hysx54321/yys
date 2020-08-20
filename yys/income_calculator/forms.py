import random

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from income_calculator import db_accessor


def get_period_choices():
    choices = []
    periods = db_accessor.get_active_periods()
    for period in periods:
        choices.append((
            period.id, period
        ))
    return choices


def get_item_choices_for_creating_event_entity(event):
    items = db_accessor.get_active_items()
    existing_event_entities = db_accessor.get_event_entities_by_event_id(event.id)
    items_to_create = []
    for item in items:
        created = False
        for entity in existing_event_entities:
            if item.id == entity.item_id:
                created = True
                break

        if not created:
            items_to_create.append((item.id, item))

    return items_to_create


class SaveGameForm(forms.Form):
    score = forms.IntegerField()
    second = forms.IntegerField()
    move = forms.IntegerField()
    reconstruction = forms.IntegerField()

    def clean_score(self):
        data = self.cleaned_data['score']

        # Check if the number is too large.
        if data > 10000 or data < 0:
            raise ValidationError(_('Invalid number - it must be between 0 and 10000'))

        # Remember to always return the cleaned data.
        return data + random.randint(1, 50)


class NewItemForm(forms.Form):
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)


class NewPeriodForm(forms.Form):
    num_days = forms.IntegerField()
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)


class NewEventForm(forms.Form):
    default_frequency = forms.IntegerField()
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)
    period_id = forms.ChoiceField(choices=get_period_choices())


class NewEventEntityForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super(NewEventEntityForm, self).__init__(*args, **kwargs)
        self.fields['item_id'].choices = get_item_choices_for_creating_event_entity(event)

    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)
    maximum = forms.IntegerField()
    minimum = forms.IntegerField()
    expectation_value = forms.IntegerField()
    item_id = forms.ChoiceField()
