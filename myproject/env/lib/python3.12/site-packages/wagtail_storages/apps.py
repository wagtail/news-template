from django import apps
from django.utils.translation import gettext_lazy as _


class WagtailStoragesConfig(apps.AppConfig):
    name = "wagtail_storages"
    verbose_name = _("Wagtail storages")

    def ready(self):
        from wagtail_storages import signal_handlers

        signal_handlers.register_signal_handlers()
