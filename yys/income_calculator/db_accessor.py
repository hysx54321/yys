from income_calculator import utils
from income_calculator.models import (
    Event,
    Item,
    Period,
)


# Event
def create_event(
    display_name,
    description,
    minimum,
    maximum,
    expectation_value,
    default_frequency,
    comment,
    period_id,
    item_id,
    priority=1,
    icon="",
):
    new_event = Event(
        display_name=display_name,
        description=description,
        min=minimum,
        max=maximum,
        expectation_value=expectation_value,
        default_frequency=default_frequency,
        default_total=default_frequency * expectation_value,
        comment=comment,
        period_id=period_id,
        item_id=item_id,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        priority=priority,
        icon=icon,
        deleted=False,
    )
    new_event.save()


def get_event_by_id(event_id):
    event = Event.objects.filter(id=event_id)
    if event and not event[0].deleted:
        return event[0]
    return None


def get_event_by_period_id(period_id):
    return Event.objects.filter(period_id=period_id)


def get_event_by_period_id_and_item_id(period_id, item_id):
    return Event.objects.filter(period_id=period_id, item_id=item_id)


# Item
def create_item(description, comment):
    new_item = Item(
        description=description,
        comment=comment,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_item.save()


def get_item_by_id(item_id):
    item = Item.objects.filter(id=item_id)
    if item and not item[0].deleted:
        return item[0]
    return None


def get_items(**kwargs):
    return Item.objects.filter(**kwargs)


# Period
def create_period(description, comment, num_days):
    new_period = Period(
        num_days=num_days,
        description=description,
        comment=comment,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_period.save()


def get_period_by_id(period_id):
    period = Period.objects.filter(id=period_id)
    if period and not period[0].deleted:
        return period[0]
    return None


def get_periods(**kwargs):
    return Period.objects.filter(**kwargs)
