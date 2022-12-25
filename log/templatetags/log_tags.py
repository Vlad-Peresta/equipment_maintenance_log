from django import template

from log.models import Breakdown, Equipment

register = template.Library()


@register.simple_tag
def active_failures_amount():
    return Breakdown.objects.filter(status="process").count()


@register.simple_tag
def equipment_number():
    return Equipment.objects.all().count()
