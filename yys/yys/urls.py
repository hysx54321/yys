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

    # path('events/', views.event_list, name='events'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/delete', views.delete_event, name='event_delete'),
    path('event/<int:event_id>/edit', views.update_event, name='event_edit'),
    path('event/<int:event_id>/new_entity', views.new_event_entity, name='new_event_entity'),
    path('event/new', views.new_event, name='new_event'),

    path('event_entities/<int:event_entity_id>/edit', views.update_event_entity, name='event_entity_edit'),
    path('event_entity/delete', views.delete_event_entity, name='event_entity_delete'),

    path('event_groups/', views.delete_item, name='event_groups'),

    path('items/', views.ItemListView.as_view(), name='items'),
    path('item/new', views.new_item, name='new_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/delete', views.delete_item, name='item_delete'),
    path('item/<int:item_id>/edit', views.update_item, name='item_edit'),

    path('periods/', views.PeriodListView.as_view(), name='periods'),
    path('period/new', views.new_period, name='new_period'),
    path('period/<int:pk>/', views.PeriodDetailView.as_view(), name='period_detail'),
    path('period/<int:period_id>/edit', views.update_period, name='period_edit'),
    path('period/delete', views.delete_period, name='period_delete'),

    path('speed_calculator/', views.speed_calculator, name='speed_calculator'),
    path('speed_calculator/tuila', views.speed_calculator, name='tuila'),
    path('speed_calculator/baimian', views.speed_calculator, name='baimian'),
]
