from django import template

register = template.Library()


def shit(value, arg):
    return value.replace(arg, '')


def cut(value):
    return value+1
