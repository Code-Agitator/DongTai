from dongtai_common.common.utils import DongTaiAppConfigPatch
from django.apps import AppConfig


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = "dongtai_web"

    def ready(self):
        super().ready()
#        register_preheat()
        from dongtai_conf.celery import app as celery_app
        from dongtai_common.utils.validate import validate_hook_strategy_update
        from deploy.commands.management.commands.load_hook_strategy import Command
        from dongtai_conf.settings import AUTO_UPDATE_HOOK_STRATEGY
        if AUTO_UPDATE_HOOK_STRATEGY and not validate_hook_strategy_update():
            print("enable auto_update_hook_strategy  updating hook strategy from file")
            Command().handle()

# def register_preheat():
#    from dongtai_engine.preheat import PreHeatRegister
#
#    from dongtai_web.aggr_vul.app_vul_summary import get_annotate_cache_data
#
#    PreHeatRegister.register(get_annotate_cache_data)
