from django.db import models
from django.utils import timezone

class Consommable(models.Model):
    nom_consommable = models.CharField(max_length=20, verbose_name="nom de consommable")
    type_consommable = models.CharField(max_length=50, verbose_name="tyde de consommable")
    mode_consommation = models.CharField(max_length=10, verbose_name="mode de consommation")
    created_at_consommation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    def __str__(self) :
        return f"{self.nom_consommable} {self.type_consommable} {self.mode_consommation}"

    class Meta:
        db_table = "Consommable"
        verbose_name = "consommable"
        verbose_name_plural = "consommables"
# Create your models here.
