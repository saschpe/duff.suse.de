# -*- coding: utf-8 -*-

from django import template

from ..models import Service


register = template.Library()

@register.filter
def service_running_color(running):
    """Returns Bootstrap-compatible contextual color CSS class from Service state.
    """
    if running:
        return "success"
    else:
        return "error"
