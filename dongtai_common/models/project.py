#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:32
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_common.models import User
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_common.utils.settings import get_managed
import time


class VulValidation(models.IntegerChoices):
    FOLLOW_GLOBAL = 0
    ENABLE = 1
    DISABLE = 2
    __empty__ = 0


class IastProject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    mode = models.CharField(default="插桩模式",
                            max_length=255,
                            blank=True,
                            null=True)
    vul_count = models.PositiveIntegerField(blank=True, null=True)
    agent_count = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(default=lambda: int(time.time()),
                                      blank=True,
                                      null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    # openapi服务不必使用该字段
    scan = models.ForeignKey(IastStrategyUser,
                             models.DO_NOTHING,
                             blank=True,
                             null=True)

    vul_validation = models.IntegerField(default=0,
                                         blank=True,
                                         null=False,
                                         choices=VulValidation.choices)
    base_url = models.CharField(max_length=255, blank=True, default='')
    test_req_header_key = models.CharField(max_length=511,
                                           blank=True,
                                           default='')
    test_req_header_value = models.CharField(max_length=511,
                                             blank=True,
                                             default='')
    data_gather = models.JSONField()
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_project'

    def update_latest(self):
        self.latest_time = int(time.time())
        self.save(update_fields=['latest_time'])


class IastProjectTemplate(models.Model):
    template_name = models.CharField(max_length=255, blank=True, null=True)
    latest_time = models.IntegerField(default=lambda: int(time.time()),
                                      blank=True,
                                      null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    scan = models.ForeignKey(IastStrategyUser,
                             models.DO_NOTHING,
                             blank=True,
                             null=True)
    vul_validation = models.IntegerField(default=0,
                                         blank=True,
                                         null=False,
                                         choices=VulValidation.choices)
    is_system = models.IntegerField(default=0)
    data_gather = models.JSONField(default=dict)
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_project_template'

    def to_full_template(self):
        pass
