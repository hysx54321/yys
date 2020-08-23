from django import template

register = template.Library()


@register.filter
def get_object_by_id(value, period_id):
    for p in value:
        if p.id == period_id:
            return p


@register.filter
def get_attribute(obj, attribute):
    """ Try to get an attribute from an object.

    Example: {% if block|getattr:"editable,True" %}

    Beware that the default is always a string, if you want this
    to return False, pass an empty second argument:
    {% if block|getattr:"editable," %}
    """
    try:
        return obj.__getattribute__(attribute)
    except AttributeError:
        return obj.__dict__.get(attribute, None)
    except:
        return None
