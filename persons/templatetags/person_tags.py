from django import template
from persons.models import Task

register = template.Library()


@register.simple_tag
def task_count(person_id):
    return Task.objects.filter(person_id=person_id).count()
