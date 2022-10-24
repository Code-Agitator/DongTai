#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午6:38
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_common.models.user import User
from time import time


class HookType(models.Model):
    type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    enable = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True, default=time)
    update_time = models.IntegerField(blank=True, null=True, default=time)
    created_by = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey(IastProgramLanguage,
                                 blank=True,
                                 default='',
                                 on_delete=models.DO_NOTHING,
                                 db_constraint=False)
    vul_strategy = models.ForeignKey(
        'dongtai_common.IastStrategyModel',
        blank=True,
        default=-1,
        null=True,
        on_delete=models.DO_NOTHING,
        db_column='strategy_id',
        db_constraint=False,
    )
    system_type = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = get_managed()
        db_table = 'iast_hook_type'
