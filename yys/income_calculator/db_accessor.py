from income_calculator import utils
from income_calculator.models import (
    Event,
    Item,
    Period,
    EventEntity,
    EventGroup,
)


# Event
def create_event(
    display_name,
    description,
    default_frequency,
    comment,
    period_id,
    item_id,
    event_group_id=None,
    priority=1,
    icon="",
):
    new_event = Event(
        display_name=display_name,
        description=description,
        default_frequency=default_frequency,
        comment=comment,
        period_id=period_id,
        item_id=item_id,
        event_group_id=event_group_id,
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


# Event Entity
def create_event_entity(
    event,
    display_name,
    description,
    minimum,
    maximum,
    expectation_value,
    comment,
    item_id,
):
    new_event_entity = EventEntity(
        display_name=display_name,
        description=description,
        min=minimum,
        max=maximum,
        expectation_value=expectation_value,
        default_total=event.default_frequency * expectation_value,
        comment=comment,
        item_id=item_id,
        event_id=event.id,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_event_entity.save()


def get_event_entity_by_id(event_entity_id):
    event_entity = EventEntity.objects.filter(id=event_entity_id)
    if event_entity and not event_entity[0].deleted:
        return event_entity[0]
    return None


def get_event_entities_by_event_id(event_id):
    return EventEntity.objects.filter(event_id=event_id)


def get_event_entities_by_period_id_and_item_id(period_id, item_id):
    return EventEntity.objects.filter(period_id=period_id, item_id=item_id)


# Event Group
def create_event_group(description, comment):
    new_event_group = EventGroup(
        description=description,
        comment=comment,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_event_group.save()


def get_event_group_by_id(event_group_id):
    event_group = EventGroup.objects.filter(id=event_group_id)
    if event_group and not event_group[0].deleted:
        return event_group[0]
    return None


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
    return new_item


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
