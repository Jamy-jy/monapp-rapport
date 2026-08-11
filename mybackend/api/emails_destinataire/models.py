from django.db import models
from django.utils import timezone

class Emails_destinataire(models.Model):
    nom_proprietaire = models.CharField(max_length=20, verbose_name="nom du propriétaire de l\'email")
    emails_destiny = models.CharField(max_length=100, verbose_name="adresse email destinataire")
    email_created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création de l'email")

    def __str__(self) :
        return f"{self.nom_proprietaire} {self.emails_destiny}"

    class Meta:
        db_table = "emails_destinataire"
        verbose_name = "email_destinataire"
        verbose_name_plural = "emails_destinataires"

# Create your models here.
