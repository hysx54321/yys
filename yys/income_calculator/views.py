from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# Create your views here.
from django.views import generic

from income_calculator import db_accessor
from income_calculator.forms import ItemForm, PeriodForm, EventForm, EventEntityForm
from income_calculator.models import (
    Event,
    Item,
    Period,
    EventEntity)


class Object(object):
    pass


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_events = len(db_accessor.get_active_events())
    num_items = len(db_accessor.get_active_items())
    num_periods = len(db_accessor.get_active_periods())

    context = {
        'num_events': num_events,
        'num_items': num_items,
        'num_periods': num_periods,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def delete_item(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('items'))
    item = get_object_or_404(Item, id=request.POST.get('item_id'))

    db_accessor.delete_item(item.id)
    messages.add_message(request, messages.INFO, 'Successfully deleted ' + str(item))
    return HttpResponseRedirect(reverse('items'))


def new_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = db_accessor.create_item(
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('item_detail', kwargs={'pk': item.id}))
    else:
        form = ItemForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


def update_item(request, item_id):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            db_accessor.update_item(
                item_id,
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('item_detail', kwargs={'pk': item_id}))
    else:
        item = db_accessor.get_item_by_id(item_id)
        form = ItemForm(initial={
                'display_name': item.display_name,
                'comment': item.comment,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 5

    def get_queryset(self):
        items = db_accessor.get_active_items()
        if items:
            return items.order_by('-time_modified')
        return items


def item_detail(request, item_id):
    item = db_accessor.get_item_by_id(item_id)
    periods = db_accessor.get_active_periods()
    events = None
    wanted_event_entities = []
    total_income = 0
    if request.GET.get('period_id'):
        print('hello')
        period_id = int(request.GET['period_id'])
        events = db_accessor.get_active_events(period_id=period_id)
        for event in events:
            event_entities = db_accessor.get_event_entities_by_event_id_and_item_id(event.id, item_id)
            if event_entities:
                event_entity = event_entities[0]
                wanted_event_entities.append(event_entity)
                total_income += event.default_frequency * event_entity.expectation_value

    context = {
        'item_detail': item,
        'periods': periods,
        'events': events,
        'event_entities': wanted_event_entities,
        'total_income': total_income,
    }
    return render(request, 'income_calculator/item_detail.html', context)


def new_period(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            period = db_accessor.create_period(
                num_days=form.cleaned_data['num_days'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('period_detail', kwargs={'pk': period.id}))
    else:
        form = PeriodForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_period.html', context)


def update_period(request, period_id):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            db_accessor.update_period(
                period_id,
                num_days=form.cleaned_data['num_days'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('period_detail', kwargs={'pk': period_id}))
    else:
        period = db_accessor.get_period_by_id(period_id)
        form = PeriodForm(initial={
                'num_days': period.num_days,
                'display_name': period.display_name,
                'comment': period.comment,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


class PeriodListView(generic.ListView):
    model = Period
    paginate_by = 5

    def get_queryset(self):
        periods = db_accessor.get_active_periods()
        if periods:
            return periods.order_by('num_days')
        return periods


class PeriodDetailView(generic.DetailView):
    model = Period
    context_object_name = 'period_detail'


def delete_period(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('periods'))
    period = get_object_or_404(Period, id=request.POST.get('period_id'))

    db_accessor.delete_period(period.id)
    messages.add_message(request, messages.INFO, 'Successfully deleted ' + str(period))
    return HttpResponseRedirect(reverse('periods'))


class EventDetailView(generic.DetailView):
    model = Event
    context_object_name = 'event_detail'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get periods
        periods = db_accessor.get_active_periods()
        context['periods'] = periods

        # Get event entities
        event_entities = db_accessor.get_event_entities_by_event_id(event_id=self.kwargs['pk'])
        context['event_entity_list'] = event_entities

        # Get Items
        items = db_accessor.get_active_items()
        context['items'] = items

        return context


class EventListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('period_id'):
            events = db_accessor.get_active_events(period_id=self.request.GET['period_id'])
        else:
            events = db_accessor.get_active_events()

        if events:
            return events.order_by('-priority')
        return events

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        periods = db_accessor.get_active_periods()
        context['periods'] = periods
        return context


def event_list(request):
    return EventListView.as_view


def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = db_accessor.create_event(
                period_id=form.cleaned_data['period_id'],
                default_frequency=form.cleaned_data['default_frequency'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event.id}))
    else:
        form = EventForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


def update_event(request, event_id):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            db_accessor.update_event(
                event_id=event_id,
                period_id=form.cleaned_data['period_id'],
                default_frequency=form.cleaned_data['default_frequency'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event_id}))
    else:
        event = db_accessor.get_event_by_id(event_id)
        form = EventForm(initial={
                'period_id': event.period_id,
                'default_frequency': event.default_frequency,
                'display_name': event.display_name,
                'comment': event.comment,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


def delete_event(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('events'))
    event = get_object_or_404(Event, id=request.POST.get('event_id'))

    db_accessor.delete_event(event.id)
    messages.add_message(request, messages.INFO, 'Successfully deleted ' + str(event))
    return HttpResponseRedirect(reverse('events'))


def new_event_entity(request, event_id):
    event = db_accessor.get_event_by_id(event_id)
    if request.method == 'POST':
        form = EventEntityForm(event, None, request.POST)
        if form.is_valid():
            event_entity = db_accessor.create_event_entity(
                event=event,
                item_id=form.cleaned_data['item_id'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
                maximum=form.cleaned_data['maximum'],
                minimum=form.cleaned_data['minimum'],
                expectation_value=form.cleaned_data['expectation_value'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event.id}))
    else:
        form = EventEntityForm(initial={'comment': "ywdltql"}, event=event, existing_event_entity=None)
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)


def delete_event_entity(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('events'))
    event_entity = get_object_or_404(EventEntity, id=request.POST.get('event_entity_id'))

    db_accessor.delete_event_entity(event_entity.id)
    messages.add_message(request, messages.INFO, 'Successfully deleted ' + str(event_entity))
    return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event_entity.event_id}))


def update_event_entity(request, event_entity_id):
    event_entity = db_accessor.get_event_entity_by_id(event_entity_id)
    event = db_accessor.get_event_by_id(event_entity.event_id)
    if request.method == 'POST':
        form = EventEntityForm(event, event_entity, request.POST)
        if form.is_valid():
            db_accessor.update_event_entity(
                event_entity_id=event_entity_id,
                item_id=form.cleaned_data['item_id'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
                max=form.cleaned_data['maximum'],
                min=form.cleaned_data['minimum'],
                expectation_value=form.cleaned_data['expectation_value'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event_entity.event_id}))
    else:
        form = EventEntityForm(
            event,
            event_entity,
            initial={
                'item_id': event_entity.item_id,
                'display_name': event_entity.display_name,
                'comment': event_entity.comment,
                'maximum': event_entity.max,
                'minimum': event_entity.min,
                'expectation_value': event_entity.expectation_value,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/generic_form.html', context)
