#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Bidaya0
# datetime:2021/7/27 11:36
# software: Vim8
# project: webapi

import time
from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.deploy import IastDeployDesc
from dongtai_common.models.system import IastSystem
from rest_framework.authtoken.models import Token
from dongtai_web.utils import get_model_field
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer



class AgentDeployArgsSerializer(serializers.Serializer):
    middleware = serializers.CharField(required=False)
    language = serializers.CharField(required=False)


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(((201, _("Corresponding deployment document could not be found")), ''), ))

class AgentDeploy(UserEndPoint):
    @extend_schema_with_envcheck([AgentDeployArgsSerializer],
                                 tags=[_('Documents')],
                                 summary=_('Document of Agent Deploy'),
                                 description=_("Document of Agent Deploy"),
                                 response_schema=_ResponseSerializer)
    def get(self, request):
        ser = AgentDeployArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        desc = IastDeployDesc.objects.filter(**ser.validated_data).first()
        if desc:
            return R.success(data=model_to_dict(desc))
        return R.failure(
            msg=_("Corresponding deployment document could not be found"))
