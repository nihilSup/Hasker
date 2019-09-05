from django import template

import json

register = template.Library()


@register.filter
def as_votes_json(votable, user):
    return json.dumps(dict(
        user_ups=votable.user_ups(user),
        user_downs=votable.user_downs(user),
        votes=(votable.votes)
    ))
