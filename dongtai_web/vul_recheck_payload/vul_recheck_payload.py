import time

from dongtai_common.endpoint import UserEndPoint, R, TalentAdminEndPoint
from dongtai_common.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent_config import AgentConfigSettingSerializer
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from dongtai_common.models.vul_recheck_payload import IastVulRecheckPayload
from rest_framework import serializers
from django.db.models import Q
from django.forms.models import model_to_dict


def get_or_none(classmodel, function, **kwargs):
    try:
        if function:
            return function(classmodel.objects).get(**kwargs)
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class IastVulRecheckPayloadSerializer(serializers.Serializer):
    value = serializers.CharField()
    status = serializers.IntegerField()
    strategy_id = serializers.IntegerField()
    language_id = serializers.IntegerField()


class IastVulRecheckPayloadListSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False, default=None)
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    strategy_id = serializers.IntegerField(required=False, default=None)
    language_id = serializers.IntegerField(required=False, default=None)


def vul_recheck_payload_create(data, user_id):
    IastVulRecheckPayload.objects.create(strategy_id=data['strategy_id'],
                                         user_id=user_id,
                                         value=data['value'],
                                         status=data['status'],
                                         language_id=data['language_id'])


class AgentConfigSettingBatchV2Serializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


def payload_update(pk, data):
    IastVulRecheckPayload.objects.filter(pk=pk).update(**data)


class VulReCheckPayloadViewSet(UserEndPoint, viewsets.ViewSet):
    name = "api-v1-vul-recheck-payload"
    description = _("config recheck payload V2")

    def create(self, request):
        ser = IastVulRecheckPayloadSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        vul_recheck_payload_create(ser.data, request.user.id)
        return R.success()

    def retrieve(self, request, pk):
        obj = get_or_none(
            IastVulRecheckPayload,
            lambda x: x.values('id', 'user__username', 'strategy__vul_name',
                               'value', 'user_id', 'strategy_id', 'status',
                               'create_time', 'language_id'),
            pk=pk, user_id=request.user.id)
        if obj is None:
            return R.failure()
        return R.success(data=obj)

    def list(self, request):
        ser = IastVulRecheckPayloadListSerializer(data=request.query_params)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q(user_id=request.user.id) & ~Q(status=-1)
        keyword = ser.data['keyword']
        strategy_id = ser.data['strategy_id']
        language_id = ser.data['language_id']
        page = ser.data['page']
        page_size = ser.data['page_size']
        if keyword:
            q = q & Q(value__icontains=keyword)
        if strategy_id:
            q = q & Q(strategy_id=strategy_id)
        if language_id:
            q = q & Q(language_id=language_id)
        queryset = IastVulRecheckPayload.objects.filter(q).order_by(
            '-create_time').values('id', 'user__username',
                                   'strategy__vul_name', 'value', 'user_id',
                                   'strategy_id', 'status', 'create_time',
                                   'language_id')
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(page=page_summary,
                         data=list(page_data))

    def update(self, request, pk):
        ser = IastVulRecheckPayloadSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        if IastVulRecheckPayload.objects.filter(
                pk=pk, user_id=request.user.id).exists():
            payload_update(pk, ser.data)
            return R.success()
        return R.success()

    def delete(self, request, pk):
        if IastVulRecheckPayload.objects.filter(
                pk=pk, user_id=request.user.id).exists():
            IastVulRecheckPayload.objects.filter(pk=pk).update(status=-1)
            return R.success()
        return R.failure()

    def status_change(self, request):
        mode = request.data.get('mode', 1)
        q = ~Q(status=-1) & Q(user_id=request.user.id)
        if mode == 1:
            ids = request.data.get('ids', [])
            status = request.data.get('status', 0)
            q = q & Q(pk__in=ids)
            IastVulRecheckPayload.objects.filter(q).update(status=status)
        elif mode == 2:
            status = request.data.get('status', 0)
            q = q
            IastVulRecheckPayload.objects.filter(q).update(status=status)
        return R.success()

    def status_all(self, request):
        status = request.data.get('status', 0)
        q = ~Q(status=-1)
        IastVulRecheckPayload.objects.filter(q).update(status=status)
        return R.success()
