from django.apps import AppConfig


class FormsConfig(AppConfig):
    default_auto_field: str = "django.db.models.AutoField"
    name = "{{ project_name }}.forms"
