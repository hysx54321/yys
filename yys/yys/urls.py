"""yys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from income_calculator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/delete', views.delete_item, name='event_delete'),
    path('event/<int:event_id>/edit', views.delete_item, name='event_edit'),
    path('event/<int:event_id>/event_entities', views.EventEntitiesByEventView.as_view(), name='event_entities_by_event'),
    path('event/<int:event_id>/new_entity', views.new_event_entity, name='new_event_entity'),
    path('new_event/', views.new_event, name='new_event'),
    path('event_entities/', views.delete_item, name='event_entities'),
    path('event_groups/', views.delete_item, name='event_groups'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('new_item/', views.new_item, name='new_item'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('item/delete', views.delete_item, name='item_delete'),
    path('item/<int:item_id>/edit', views.delete_item, name='item_edit'),
    path('periods/', views.PeriodListView.as_view(), name='periods'),
    path('new_period/', views.new_period, name='new_period'),
    path('period/<int:pk>/', views.PeriodDetailView.as_view(), name='period_detail'),
    path('period/<int:item_id>/edit', views.delete_item, name='period_edit'),
    path('period/delete', views.delete_period, name='period_delete'),
]
