from django.apps import AppConfig


class DuplicateConfig(AppConfig):
    name = 'duplicate'

    def ready(self):
        import duplicate.signals