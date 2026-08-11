from django.db import models
from django.utils import timezone


class RapportJournal(models.Model):
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    email_destiny = models.TextField(verbose_name="Destinataires")
    cc = models.CharField(max_length=255, blank=True, default='')
    cci = models.CharField(max_length=255, blank=True, default='')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    objet = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    fichier = models.FileField(upload_to="rapports/", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rapport {self.date_debut} - {self.date_fin}"

    class Meta:
        db_table = "RapportJournal"

class RapportJournalLu(models.Model):
    rapport = models.ForeignKey(RapportJournal, on_delete=models.CASCADE, related_name='lectures')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    lu_at = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False, verbose_name="Supprimé")  # ← ajouter

    class Meta:
        db_table = "RapportJournalLu"
        unique_together = ('rapport', 'user')

    def __str__(self):
        return f"{self.user.email} a lu {self.rapport.id}"
    

class TextModel(models.Model):
    text = models.CharField(max_length=255)
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "Modele"
        
    def __str__(self):
        return self.text

# Create your models here.
