import uuid
from django.db import models
from django.utils import timezone

class Site(models.Model):
    user = models.ForeignKey(
            'users.User',
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
        )
    nom_site = models.CharField(max_length=100)
    accronyme_site = models.CharField(max_length=10)
    site_created_at = models.DateTimeField(default=timezone.now)

    class Meta:
            db_table = "site"

class GroupInventaire(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    site = models.ForeignKey('site', null=True,
            blank=True, on_delete=models.CASCADE)
    nom_group = models.CharField(max_length=100)
    access_group = models.BooleanField(default=False)
    group_created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "Groupe_inventaire"

class ComposantGroup(models.Model):
    group = models.ForeignKey('GroupInventaire', on_delete=models.CASCADE)
    nom_materiel = models.CharField(max_length=100)
    marque_materiel = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    configuration = models.CharField(max_length=255)
    Etat_materiel = models.BooleanField(null=True)
    composant_created_at = models.DateTimeField(default=timezone.now)
    test_fonctionnalite = models.TextField(null=True, blank=True,)

    # --- champs pour le remplacement ---
    lineage_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    remplace = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='remplacant',
        help_text="Ancien matériel que cette ligne remplace"
    )
    date_remplacement = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Composant_groupe"
# Create your models here.
