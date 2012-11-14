from django import template

from ..models import Domain


register = template.Library()

@register.filter
def domain_state_color(state):
    """Returns Twitter Bootstrap contextual color classes by Domain state.
    """
    if state == Domain.RUNNING:
        return "success"
    elif state == Domain.SHUTOFF or state == Domain.SHUTDOWN:
        return "warning"
    elif state == Domain.CRASHED or state == Domain.BLOCKED:
        return "error"
    else:
        return "info"
