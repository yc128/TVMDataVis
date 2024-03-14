from django.apps import AppConfig


class TvmvisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tvmvis'

    def ready(self):
        import sys
        if 'runserver' in sys.argv:
            from .data_manager.store_json_to_db import store_json_to_db
            store_json_to_db()
