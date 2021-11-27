from django.apps import AppConfig


class PluginsMarketBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'datamap'
    url_prefix = "datamap",
