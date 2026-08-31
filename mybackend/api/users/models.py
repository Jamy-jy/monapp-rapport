from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

def validate_phone(phone: str):
    """
    FIX : validation corrigée du numéro malgache, dans les 2 formats acceptés :
    - Local        : 0XXXXXXXXX      (0 + 9 chiffres)
    - International: +261XXXXXXXXX   (+261 + 9 chiffres)
    Retourne (is_valid, error_message)
    """
    if not phone:
        return 

    #supprime les espace et compter les chiffres
    raw = phone.replace(' ', '').replace('-', '')

    if raw.startswith('+261'):
        digits = raw[4:]
        if not digits.isdigit():
            raise ValidationError("Le numéro doit contenir uniquement des chiffres après +261")
        diff = 9 - len(digits)
        if diff > 0:
            raise ValidationError(f"Il manque {diff} chiffre(s) après +261 (9 attendus)")
        if diff < 0:
            raise ValidationError(f"Il y a {-diff} chiffre(s) en trop après +261 (9 attendus)")
        return 

    if raw.startswith('0'):
        if not raw.isdigit():
            raise ValidationError("Le numéro doit contenir uniquement des chiffres")
        digits = raw[1:]
        diff = 9 - len(digits)
        if diff > 0:
            raise ValidationError(f"Il manque {diff} chiffre(s) (9 attendus après le 0)")
        if diff < 0:
            raise ValidationError(f"Il y a {-diff} chiffre(s) en trop (9 attendus après le 0)")
        return 

    raise ValidationError("Le numéro doit commencer par 0 ou +261")

def check_phone(phone: str):
    """
    >>> AJOUT : version "tuple" de la validation, dédiée à un usage manuel
    dans les vues (ex: update()). Ne remplace PAS validate_phone (le validator
    Django), qui lui doit continuer à `raise`.
    Retourne (is_valid: bool, error_message: str | None)
    """
    try:
        validate_phone(phone)
        return True, None
    except ValidationError as e:
        return False, e.message

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
        max_length=20,
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
