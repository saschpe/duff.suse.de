# Copyright 2012 Sascha Peilicke <saschpe@gmx.de>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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
