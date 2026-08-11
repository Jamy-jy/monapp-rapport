from django.db import models
from django.utils import timezone
from django.db.models import Q, UniqueConstraint


class Stock_consommable(models.Model):
    consommable = models.ForeignKey('consommables.Consommable', on_delete=models.CASCADE)
    qte_entree = models.IntegerField()
    qte_sortie = models.IntegerField()
    qte_restant = models.IntegerField() 
    date_mouvement = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Technicien"
    )

    def __str__(self):
        return f"Stock {self.consommable.nom_consommable}"
    
    class Meta:
        db_table = "Stock_consommable"

class BoxPaf(models.Model):
    numero_boxPaf = models.CharField(max_length=100)

    def __str__(self) :
        return f"{self.numero_boxPaf}"

    class Meta:
        db_table = "BoxPaf"

class BoxOp(models.Model):
    numero_boxOp = models.CharField(max_length=100)

    def __str__(self) :
        return f"{self.numero_boxOp}"

    class Meta:
        db_table = "BoxOp"

class Bobine(models.Model):
    consommable = models.ForeignKey('consommables.Consommable',on_delete=models.CASCADE,
        limit_choices_to={'type_consommable': 'Bobine'},
    )

    numero_bobine = models.CharField(max_length=100)
    debut_serie = models.BigIntegerField()
    fin_serie = models.BigIntegerField()
    est_terminee = models.BooleanField(default=False)
    box_paf = models.ForeignKey(BoxPaf,on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_assignation = models.DateTimeField(default=timezone.now)
    date_modif = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.numero_bobine
    
    class Meta:
        db_table = "Bobine"
        constraints = [
            UniqueConstraint(
                fields=['box_paf'],
                condition=Q(est_terminee=False),
                name='unique_active_bobine_par_box'
            )
        ]

class Vignettes(models.Model):
    num_bobine = models.ForeignKey(Bobine,on_delete=models.CASCADE,related_name="vignettes")
    num_debutVignette = models.BigIntegerField()
    num_FinVignette = models.BigIntegerField()
    nb_abime = models.IntegerField()
    cause = models.CharField(max_length=255, blank=True)
    date_modif = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        return f"{self.cause}"

    class Meta:
        db_table = "Vignette"

class Imprimante(models.Model):
    boxOp = models.ForeignKey('BoxOp', on_delete=models.CASCADE)
    nb_copie = models.IntegerField()
    date_prise = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        return f"{self.boxOp}"
    
    class Meta:
        db_table = "Imprimante"

class RapportStock(models.Model):
    rapport = models.ForeignKey('myrapport.RapportJournal', on_delete=models.CASCADE)
    consommable = models.ForeignKey('consommables.Consommable', on_delete=models.CASCADE)
    qte_entree = models.IntegerField()
    qte_sortie = models.IntegerField()
    qte_restant = models.IntegerField()

    class Meta:
        db_table = "RapportStock"

class RapportBobine(models.Model):
    rapport = models.ForeignKey('myrapport.RapportJournal', on_delete=models.CASCADE, related_name="bobines")

    box_paf = models.ForeignKey(BoxPaf, on_delete=models.SET_NULL, null=True)

    numero_bobine = models.CharField(max_length=100)

    debut_serie = models.BigIntegerField()
    fin_serie = models.BigIntegerField()

    est_terminee = models.BooleanField()

    class Meta:
        db_table = "RapportBobine"

class RapportVignette(models.Model):
    rapport = models.ForeignKey('myrapport.RapportJournal', on_delete=models.CASCADE, related_name="vignettes")

    box_paf = models.ForeignKey(BoxPaf, on_delete=models.SET_NULL, null=True)

    num_debut = models.BigIntegerField()
    num_fin = models.BigIntegerField()

    nb_abime = models.IntegerField()

    class Meta:
        db_table = "RapportVignette"

class RapportImpression(models.Model):
    rapport = models.ForeignKey('myrapport.RapportJournal', on_delete=models.CASCADE, related_name="impressions")

    box = models.ForeignKey(BoxOp, on_delete=models.CASCADE)

    nb_copie = models.IntegerField()

    class Meta:
        db_table = "RapportImpression"

#encre pour imprimante
class CouleurEncre(models.Model):
    nom = models.CharField(max_length=50)        # Noir, Bleu, Rouge, Jaune
    reserve = models.IntegerField(default=0)     # nombre de bouteilles en stock

    def __str__(self):
        return self.nom

    class Meta:
        db_table = "CouleurEncre"


class NiveauEncre(models.Model):
    NIVEAUX = [
        (100, 'Plein'),
        (75,  '75%'),
        (50,  '50%'),
        (25,  '25%'),
        (0,   'Vide'),
    ]

    boxOp = models.ForeignKey('BoxOp', on_delete=models.CASCADE)
    couleur = models.ForeignKey(CouleurEncre, on_delete=models.CASCADE)
    niveau = models.IntegerField(choices=NIVEAUX, default=100)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "NiveauEncre"
        unique_together = ('boxOp', 'couleur')  # ← 1 niveau par boxOp par couleur

    def __str__(self):
        return f"{self.boxOp} - {self.couleur} - {self.niveau}%"

class StockBureau(models.Model):
    consommable = models.ForeignKey('consommables.Consommable', on_delete=models.CASCADE)
    qte_entree_bureau = models.IntegerField()
    qte_envoye_bureau = models.IntegerField()
    qte_restant_bureau = models.IntegerField() 
    nom_site = models.CharField(max_length=10, null=True, blank=True)
    date_mouvement_bureau = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Stock {self.consommable.nom_consommable}"
    
    class Meta:
        db_table = "Stock_Bureau"

class TransfertStock(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]

    consommable = models.ForeignKey('consommables.Consommable', on_delete=models.CASCADE)
    quantite = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    admin_expediteur = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True,
        related_name='transferts_envoyes'
    )
    tech_receveur = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transferts_recus'
    )

    stock_bureau_source = models.ForeignKey(
        'StockBureau', on_delete=models.SET_NULL, null=True, blank=True
    )

    date_envoi = models.DateTimeField(default=timezone.now)
    date_validation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transfert {self.consommable.nom_consommable} ({self.statut})"

    class Meta:
        db_table = "Transfert_Stock"
# Create your models here.
