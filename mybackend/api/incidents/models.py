from django.db import models
from django.utils import timezone

class Systeme(models.Model):
    titre_systeme = models.CharField(max_length=50, verbose_name="titre incident systeme")
    solution_incident_système = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    fichier_solution = models.FileField(       
        upload_to='solution/',
        null=True,
        blank=True,
        verbose_name="Fichier solution"
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"systeme {self.titre_système}"
    
    class Meta:
        db_table = "Incident_systeme"
    
class Materiels(models.Model):
    titre_incident = models.CharField(max_length=50, null=True)
    nom_materiel = models.CharField(max_length=100)
    box_paf = models.ForeignKey(
        'stock_consommables.BoxPaf',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    box_op = models.ForeignKey(
        'stock_consommables.BoxOp',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    solution_incident_materiel = models.TextField(null=True, blank=True)
    fichier_solution = models.FileField(       
        upload_to='solution/',
        null=True,
        blank=True,
        verbose_name="Fichier solution"
    )
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def Clean(self):
        from django.core.exceptions import ValidationError

        if self.box_paf and self.box_op:
            raise ValidationError(
                "Un matériel ne peut pas appartenir soit à Box Paf ou à Box Op."
            )
        
        if not self.box_op and self.box_paf:
            raise ValidationError(
                "Le matériel doit appartenir à un box."
            )
    
    class Meta:
        db_table = "Incident_materiels"
        
class Reseau(models.Model):
    nom_incident_reseau = models.CharField(max_length=50)
    solution_incident_reseau = models.TextField(null=True, blank=True)
    fichier_solution = models.FileField(       
        upload_to='solution/',
        null=True,
        blank=True,
        verbose_name="Fichier solution"
    )
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "Incident_reseau"

class IncidentSurvenu(models.Model):
    TYPE_CHOICES = [
        ('systeme', 'Système'),
        ('materiel', 'Matériel'),
        ('reseau', 'Réseau'),
    ]

    nom_incident = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description_incident = models.TextField(null=True, blank=True)
    solutionPrise = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom_incident} ({self.type})"

    class Meta:
        db_table = "IncidentSurvenu"
# Create your models here.
