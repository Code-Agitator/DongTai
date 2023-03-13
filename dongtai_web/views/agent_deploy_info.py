#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: webapi
from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.deploy import IastDeployDesc
from django.utils.translation import gettext_lazy as _


class AgentDeployInfo(UserEndPoint):
    name = "api-v1-iast-deploy-info"
    description = _("Agent deployment document")

    def get(self, request):
        condition = {
            "agents": ["Java", ".Net Core", "C#"],
            "java_version": ["Java 1.6", "Java 1.7", "Java 1.8", "Java 9", "Java 10", "Java 11", "Java 13", "Java 14",
                             "Java 15", "Java 16"],
            "middlewares": [],
            "system": ["windows", "linux"]
        }
        queryset = IastDeployDesc.objects.all()
        for item in queryset:
            if item.middleware not in condition['middlewares']:
                condition['middlewares'].append(item.middleware)
        return R.success(data=condition)
