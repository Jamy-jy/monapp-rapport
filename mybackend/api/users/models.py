from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

def validate_phone(value):
    #supprime les espace et compter les chiffres
    digits = value.replace(' ', '')
    if not digits.isdigit():
        raise ValidationError("Le numéro doit contenir uniquement des chiffres")
    if len(digits) != 10:
        raise ValidationError("Le numéro doit contenir exactement 10 chiffres")
    
class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('tech', 'Technicien'),
    ]
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='tech',verbose_name="Rôle")
    password = models.CharField(max_length=128)
    phone = models.CharField(
        max_length=13,
        verbose_name="Téléphone",
        validators=[validate_phone],
        blank=False,
        null=False,
        default=''
        )
    statut = models.BooleanField(default=True, verbose_name="Statut du compte")
    actif = models.BooleanField(default=False, verbose_name="En ligne")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    def set_password(self, raw_password):

        if len(raw_password) < 6:
            raise ValidationError("Le mot de passe doit contenir au moins 6 caractère ")
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self) :
        return f"{self.prenom} {self.nom} ({self.email}) - {self.get_role_display()}"
    
    class Meta:
        db_table = "User"
# Create your models here.
