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
def service_state_color(state):
    """Returns Bootstrap-compatible contextual color CSS class from Service state.
    """
    if state == Service.OFFLINE:
        return "error"
    elif state == Service.ONLINE:
        return "success"
    else:
        return "info"
