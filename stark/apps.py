from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StarkConfig(AppConfig):
    name = 'stark'
    def ready(self):
        print('333333333333333')
        autodiscover_modules('stark')
