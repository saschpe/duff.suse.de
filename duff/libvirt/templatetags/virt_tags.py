# -*- coding: utf-8 -*-

from django import template

from ..models import Domain, Service


register = template.Library()

@register.filter
def domain_state_color(state):
    """Returns Bootstrap-compatible contextual color CSS class from Domain state.
    """
    if state == Domain.RUNNING:
        return "success"
    elif state == Domain.SHUTOFF or state == Domain.SHUTDOWN:
        return "warning"
    elif state == Domain.CRASHED or state == Domain.BLOCKED:
        return "error"
    else:
        return "info"

@register.filter
def network_state_color(state):
    if state:
        return "success"
    else:
        return "warning"

@register.filter
def allocation_running_color(running):
    """Returns Bootstrap-compatible contextual color CSS class from Allocation running state.
    """
    if running:
        return "success"
    else:
        return "important"

@register.filter
def memsizeformat(size):
    """Returns memory size in human readable (rounded) form.
    """
    if size > 1048576: # 1024**2
      return "{0} GB".format(size / 1048576)
    elif size > 1024:
      return "{0} MB".format(size / 1024)
    else:
      return "{0} KB".format(size)
