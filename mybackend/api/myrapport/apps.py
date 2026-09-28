from django.apps import AppConfig
from django.db.models.signals import post_migrate

def seed_couleurs(sender, **kwargs):
    from .models import CouleurEncre
    CouleurEncre.objects.ensure_defaults()

class MyrapportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'myrapport'

    def ready(self):
        post_migrate.connect(seed_couleurs, sender=self)