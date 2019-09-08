import json

from django import template

register = template.Library()


@register.filter
def as_votes_json(votable, user):
    return json.dumps(dict(
        user_ups=votable.user_ups(user),
        user_downs=votable.user_downs(user),
        votes=(votable.votes)
    ))


@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)
