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


def get_item_choices_for_event_entity(event, existing_event_entity):
    items = db_accessor.get_active_items()
    existing_event_entities = db_accessor.get_event_entities_by_event_id(event.id)
    items_list = []
    for item in items:
        wanted = True
        for entity in existing_event_entities:
            if item.id == entity.item_id and (not existing_event_entity or entity.id != existing_event_entity.id):
                wanted = False
                break

        if wanted:
            items_list.append((item.id, item))

    return items_list


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


class ItemForm(forms.Form):
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)


class PeriodForm(forms.Form):
    num_days = forms.IntegerField()
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)


class EventForm(forms.Form):
    default_frequency = forms.IntegerField()
    display_name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea)
    period_id = forms.ChoiceField(label='Period', choices=get_period_choices())


class EventEntityForm(forms.Form):
    def __init__(self, event, existing_event_entity, *args, **kwargs):
        super(EventEntityForm, self).__init__(*args, **kwargs)
        self.fields['item_id'].choices = get_item_choices_for_event_entity(event, existing_event_entity)

    comment = forms.CharField(widget=forms.Textarea)
    maximum = forms.IntegerField()
    minimum = forms.IntegerField()
    expectation_value = forms.IntegerField()
    item_id = forms.ChoiceField(label='Item')

    def clean(self):
        cleaned_data = super().clean()
        maximum = cleaned_data.get("maximum")
        minimum = cleaned_data.get("minimum")
        expectation_value = cleaned_data.get("expectation_value")
        if expectation_value > maximum or expectation_value < minimum:
            raise ValidationError("Expectation should be between maximum and minimum!")
