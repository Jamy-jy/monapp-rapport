from django.db import models
from django.utils import timezone

class Vol(models.Model):
    numero_vol = models.CharField(max_length=50, unique=True)

    date_arrivee_vol = models.DateTimeField()
    date_fin_vol = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.numero_vol
    
    class Meta:
        db_table = "Vol"

class CategorieSejour(models.Model):
    libelle = models.CharField(max_length=50, null=True)      # ex: <=15 jours
    typeVisa = models.CharField(max_length=20, null=True)              # ex: 15

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = "CategorieSejour"

class Mouvement_vol(models.Model):
    num_vol = models.ForeignKey(Vol, on_delete=models.CASCADE)
    sejour = models.ForeignKey(CategorieSejour, on_delete=models.CASCADE)
    nb_par_sejour = models.IntegerField(default=0)

    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.num_vol}"

    class Meta:
        db_table = "Mouvement_vol"
        
class RapportVol(models.Model):
    rapport = models.ForeignKey('myrapport.RapportJournal', on_delete=models.CASCADE, related_name="vol")

    numero_vol = models.CharField(max_length=50)

    sejour = models.CharField(max_length=20)   # ex: <=15 kg
    nb_par_sejour = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.numero_vol} - {self.sejour}"

    class Meta:
        db_table = "RapportVol"
# Create your models here.
