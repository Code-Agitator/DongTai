#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vulnerablity import IastVulnerabilityModel

from dongtai_common.endpoint import R
from dongtai_common.endpoint import MixinAuthEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers

_ResponseSerializer = get_response_serializer(
    data_serializer=serializers.IntegerField(), )


class VulCountForPluginEndPoint(MixinAuthEndPoint):
    @extend_schema_with_envcheck(
        [
            {
                'name': "name",
                'type': str,
            },
        ],
        tags=[_('Vulnerability')],
        summary=_("Vulnerability Count (with agent name)"),
        description=_(
            "Get the number of vulnerabilities corresponding to the Agent."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        agent_name = request.query_params.get('name')
        department = request.user.get_relative_department()
        if not agent_name:
            return R.failure(msg=_("Please input agent name."))

        agent = IastAgent.objects.filter(token=agent_name,
                                         department__in=department).first()
        if not agent:
            return R.failure(msg=_("agent_name not found"))

        return R.success(
            data=IastVulnerabilityModel.objects.values('id').filter(
                agent=agent).count())
