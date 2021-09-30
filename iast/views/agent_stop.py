#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai.endpoint import UserEndPoint, R

from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from iast.serializers.agent import AgentToggleArgsSerializer 



_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(((201, _('Suspending ...')), ''), ))

class AgentStop(UserEndPoint):
    name = "api-v1-agent-stop"
    description = _("Suspend Agent")

    @extend_schema_with_envcheck(
        request=AgentToggleArgsSerializer,
        tags=[_('Agent')],
        summary=_('Agent Stop'),
        description=_(
            "Stop the running agent by specifying the id."
        ),
        response_schema=_ResponseSerializer)
    def post(self, request):
        agent_id = request.data.get('id', None)
        agent_ids = request.data.get('ids', None)
        if agent_ids:
            try:
                agent_ids = [int(i) for i in agent_ids.split(',')]
            except:
                return R.failure(_("Parameter error")) 
        if agent_id:
            agent = IastAgent.objects.filter(user=request.user,
                                             id=agent_id).first()
            if agent is None:
                return R.failure(msg=_('Engine does not exist or no permission to access'))
            if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                return R.failure(msg=_('Agent is stopping service, please try again later'))
            agent.control = 4
            agent.is_control = 1
            agent.latest_time = int(time.time())
            agent.save(update_fields=['latest_time', 'control', 'is_control'])
        if agent_ids:
            for agent_id in agent_ids:
                agent = IastAgent.objects.filter(user=request.user,
                                                 id=agent_id).first()
                if agent is None:
                    continue
                if agent.is_control == 1 and agent.control != 3 and agent.control != 4:
                    continue
                agent.control = 4
                agent.is_control = 1
                agent.latest_time = int(time.time())
                agent.save(
                    update_fields=['latest_time', 'control', 'is_control'])

        return R.success(msg=_('Suspending ...'))
