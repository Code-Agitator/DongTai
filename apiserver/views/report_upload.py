#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:45
# software: PyCharm
# project: lingzhi-agent-server

from dongtai.endpoint import OpenApiEndPoint, R
from drf_spectacular.utils import extend_schema

from apiserver.api_schema import DongTaiParameter
from apiserver.decrypter import parse_data
from apiserver.report.report_handler_factory import ReportHandler

class ReportUploadEndPoint(OpenApiEndPoint):
    name = "api-v1-report-upload"
    description = "agent上传报告"

    @extend_schema(
        description='Pull Agent Engine Hook Rule',
        parameters=[
            DongTaiParameter.LANGUAGE,
        ],
        responses=R,
        methods=['GET']
    )
    def get(self, request):
        try:
            
            #report = parse_data(request.read())
            report = {"detail":{"agentId":2690,"disk":"{}","memory":"{\"total\":\"2GB\",\"rate\":0,\"use\":\"124.115MB\"}","returnQueue":0,"cpu":"{\"rate\":53}"},"type":1}
            data = ReportHandler.handler(report, request.user)

            return R.success(msg="report upload success.", data=data)
        except Exception as e:
            return R.failure(msg=f"report upload failed, reason: {e}")
