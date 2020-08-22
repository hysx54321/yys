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
    default_frequency,
    comment,
    period_id,
    event_group_id=None,
    priority=1,
    icon="",
):
    new_event = Event(
        display_name=display_name,
        default_frequency=default_frequency,
        comment=comment,
        period_id=period_id,
        event_group_id=event_group_id,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        priority=priority,
        icon=icon,
        deleted=False,
    )
    new_event.save()
    return new_event


def get_event_by_id(event_id):
    event = Event.objects.filter(id=event_id)
    if event and not event[0].deleted:
        return event[0]
    return None


def get_events(**kwargs):
    return Event.objects.filter(**kwargs)


def get_active_events():
    return get_events(deleted=False)


def update_event(event_id, **kwargs):
    event = get_event_by_id(event_id)
    if not event:
        return
    for key, value in kwargs.items():
        setattr(event, key, value)
    event.time_modified = utils.get_current_timestamp()
    event.save()


def delete_event(event_id):
    update_event(event_id, deleted=True)


# Event Entity
def create_event_entity(
    event,
    display_name,
    minimum,
    maximum,
    expectation_value,
    comment,
    item_id,
):
    new_event_entity = EventEntity(
        display_name=display_name,
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
    return new_event_entity


def get_event_entity_by_id(event_entity_id):
    event_entity = EventEntity.objects.filter(id=event_entity_id)
    if event_entity and not event_entity[0].deleted:
        return event_entity[0]
    return None


def get_event_entities_by_event_id(event_id):
    return EventEntity.objects.filter(event_id=event_id, deleted=False)


def get_event_entities_by_period_id_and_item_id(period_id, item_id):
    return EventEntity.objects.filter(period_id=period_id, item_id=item_id)


def update_event_entity(event_entity_id, **kwargs):
    event_entity = get_event_entity_by_id(event_entity_id)
    if not event_entity:
        return
    for key, value in kwargs.items():
        setattr(event_entity, key, value)
    event_entity.time_modified = utils.get_current_timestamp()
    event_entity.save()


def delete_event_entity(event_entity_id):
    update_event_entity(event_entity_id, deleted=True)


# Event Group
def create_event_group(display_name, comment):
    new_event_group = EventGroup(
        display_name=display_name,
        comment=comment,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_event_group.save()
    return new_event_group


def get_event_group_by_id(event_group_id):
    event_group = EventGroup.objects.filter(id=event_group_id)
    if event_group and not event_group[0].deleted:
        return event_group[0]
    return None


# Item
def create_item(display_name, comment):
    new_item = Item(
        display_name=display_name,
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


def get_active_items():
    return get_items(deleted=False)


def delete_item(item_id):
    update_item(item_id, deleted=True)


def update_item(item_id, **kwargs):
    item = get_item_by_id(item_id)
    if not item:
        return
    for key, value in kwargs.items():
        setattr(item, key, value)
    item.time_modified = utils.get_current_timestamp()
    item.save()


# Period
def create_period(display_name, comment, num_days):
    new_period = Period(
        num_days=num_days,
        display_name=display_name,
        comment=comment,
        time_created=utils.get_current_timestamp(),
        time_modified=utils.get_current_timestamp(),
        deleted=False,
    )
    new_period.save()
    return new_period


def get_period_by_id(period_id):
    period = Period.objects.filter(id=period_id)
    if period and not period[0].deleted:
        return period[0]
    return None


def get_periods(**kwargs):
    return Period.objects.filter(**kwargs)


def get_active_periods():
    return get_periods(deleted=False)


def delete_period(period_id):
    update_period(period_id, deleted=True)


def update_period(period_id, **kwargs):
    period = get_period_by_id(period_id)
    if not period:
        return
    for key, value in kwargs.items():
        setattr(period, key, value)
    period.time_modified = utils.get_current_timestamp()
    period.save()
