from django import template

register = template.Library()


@register.filter
def get_object_by_id(value, period_id):
    for p in value:
        if p.id == period_id:
            return p
