from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.
from django.views import generic

from income_calculator import db_accessor
from income_calculator.forms import NewItemForm, NewPeriodForm, NewEventForm, NewEventEntityForm
from income_calculator.models import (
    Event,
    EventGroup,
    EventEntity,
    Item,
    Period,
)


class Object(object):
    pass


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_events = Event.objects.all().count()
    num_event_groups = EventGroup.objects.all().count()
    num_event_entities = EventEntity.objects.all().count()
    num_items = Item.objects.all().count()
    num_periods = len(db_accessor.get_active_periods())

    context = {
        'num_events': num_events,
        'num_event_groups': num_event_groups,
        'num_event_entities': num_event_entities,
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
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = db_accessor.create_item(display_name=form.cleaned_data['display_name'], comment=form.cleaned_data['comment'])
            return HttpResponseRedirect(reverse('item_detail', kwargs={'pk': item.id}))
    else:
        form = NewItemForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_item.html', context)


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 5

    def get_queryset(self):
        items = db_accessor.get_items(deleted=False)
        if items:
            return items.order_by('-time_modified')
        return items


class ItemDetailView(generic.DetailView):
    model = Item
    context_object_name = 'item_detail'


def new_period(request):
    if request.method == 'POST':
        form = NewPeriodForm(request.POST)
        if form.is_valid():
            period = db_accessor.create_period(
                num_days=form.cleaned_data['num_days'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('period_detail', kwargs={'pk': period.id}))
    else:
        form = NewPeriodForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_period.html', context)


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


class EventListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        events = db_accessor.get_events(deleted=False)
        if events:
            return events.order_by('-priority')
        return events

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        # self.user = get_object_or_404(User, id=self.kwargs['user_id'])
        periods = db_accessor.get_active_periods()
        context['periods'] = periods
        return context


class EventEntitiesByEventView(generic.ListView):
    model = EventEntity
    template_name = 'income_calculator/event_entities_by_event_list.html'
    context_object_name = 'event_entity_list'

    def get_queryset(self):
        event_entities = db_accessor.get_event_entities_by_event_id(self.kwargs['event_id'])
        return event_entities

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        # self.user = get_object_or_404(User, id=self.kwargs['user_id'])
        context['event'] = db_accessor.get_event_by_id(self.kwargs['event_id'])
        return context


def new_event(request):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = db_accessor.create_event(
                period_id=form.cleaned_data['period_id'],
                default_frequency=form.cleaned_data['default_frequency'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event.id}))
    else:
        form = NewEventForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_event.html', context)


def new_event_entity(request, event_id):
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = db_accessor.create_event_entity(
                period_id=form.cleaned_data['period_id'],
                default_frequency=form.cleaned_data['default_frequency'],
                display_name=form.cleaned_data['display_name'],
                comment=form.cleaned_data['comment'],
            )
            return HttpResponseRedirect(reverse('event_detail', kwargs={'pk': event.id}))
    else:
        event = db_accessor.get_event_by_id(event_id)
        form = NewEventEntityForm(initial={'comment': "ywdltql"}, event=event)
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_event.html', context)

