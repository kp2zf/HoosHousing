from django import template
from django.template.defaultfilters import stringfilter
from housing.models import Building, Unit, Review, Vote

register = template.Library()

@register.simple_tag()
def has_voted(format_string, review: Review):
    votes = review.vote_set.all()
    for vote in votes:
        if format_string == vote.username:
            return True
    return False
