from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
from django.views import generic

from income_calculator.db_accessor import create_item
from income_calculator.forms import NewItemForm
from income_calculator.models import (
    Event,
    EventGroup,
    EventEntity,
    Item,
    Period,
)


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_events = Event.objects.all().count()
    num_event_groups = EventGroup.objects.all().count()
    num_event_entities = EventEntity.objects.all().count()
    num_items = Item.objects.all().count()
    num_periods = Period.objects.all().count()

    context = {
        'num_events': num_events,
        'num_event_groups': num_event_groups,
        'num_event_entities': num_event_entities,
        'num_items': num_items,
        'num_periods': num_periods,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def dummy(request):
    return render(request, 'base_generic.html')


def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = create_item(description=form.cleaned_data['description'], comment=form.cleaned_data['comment'])
            return HttpResponseRedirect(reverse('item_detail', kwargs={'pk': item.id}))
    else:
        form = NewItemForm(initial={'comment': "ywdltql"})
    context = {
        'form': form,
    }
    return render(request, 'income_calculator/new_item.html', context)


class ItemListView(generic.ListView):
    model = Item


class ItemDetailView(generic.DetailView):
    model = Item
    context_object_name = 'item_detail'
