# Copyright (C) 2023 Sartography
#
# This file is part of SpiffWorkflow.
#
# SpiffWorkflow is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# SpiffWorkflow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
BPMN_MODEL_NS = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
#from .util import full_tag
def full_tag(tag):
    """
    Return the full tag name including namespace for the given BPMN tag. In
    other words, the name with namespace
    http://www.omg.org/spec/BPMN/20100524/MODEL
    """
    return '{%s}%s' % (BPMN_MODEL_NS, tag)
# Having this configurable via the parser makes a lot more sense than requiring a subclass
# This can be further streamlined if we ever replace our parser

SPEC_DESCRIPTIONS = {
    full_tag('startEvent'): 'Start Event',
    full_tag('endEvent'): 'End Event',
    full_tag('userTask'): 'User Task',
    full_tag('task'): 'Task',
    full_tag('subProcess'): 'Subprocess',
    full_tag('manualTask'): 'Manual Task',
    full_tag('exclusiveGateway'): 'Exclusive Gateway',
    full_tag('parallelGateway'): 'Parallel Gateway',
    full_tag('inclusiveGateway'): 'Inclusive Gateway',
    full_tag('callActivity'): 'Call Activity',
    full_tag('transaction'): 'Transaction',
    full_tag('scriptTask'): 'Script Task',
    full_tag('serviceTask'): 'Service Task',
    full_tag('intermediateCatchEvent'): 'Intermediate Catch Event',
    full_tag('intermediateThrowEvent'): 'Intermediate Throw Event',
    full_tag('boundaryEvent'): 'Boundary Event',
    full_tag('receiveTask'): 'Receive Task',
    full_tag('sendTask'): 'Send Task',
    full_tag('eventBasedGateway'): 'Event Based Gateway',
    full_tag('cancelEventDefinition'): 'Cancel',
    full_tag('errorEventDefinition'): 'Error',
    full_tag('escalationEventDefinition'): 'Escalation',
    full_tag('terminateEventDefinition'): 'Terminate',
    full_tag('messageEventDefinition'): 'Message',
    full_tag('signalEventDefinition'): 'Signal',
    full_tag('timerEventDefinition'): 'Timer',
    full_tag('conditionalEventDefinition'): 'Conditional',
}
