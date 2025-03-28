from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    date_naissance = models.CharField(max_length=20,null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_doctor = models.BooleanField(default=False)
    adresse = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    specialite = models.CharField(max_length=100, blank=True, null=True,default='') 
    def save(self, *args, **kwargs):
        self.username = self.username.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username 
    def save(self, *args, **kwargs):
        self.username = self.username.upper()
        # Efface la spécialité si l'utilisateur n'est pas médecin
        if not self.is_doctor:
            self.specialite = ''
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class DossierMedicale(models.Model):
    date_ouverture = models.DateField(auto_now_add=True) 
    medecin_responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers_medicaux_responsable', limit_choices_to={'is_doctor': True})
    patient =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers_medicaux_patient', limit_choices_to={'is_doctor': False})
    notes = models.TextField(blank=True)
    antecedents_medicaux = models.TextField(blank=True)
    medicaments_actuels = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    examens_complementaires = models.TextField(blank=True)
    
    def __str__(self):
        return f"Dossier médical pour {self.patient.username}"

class Memo(models.Model):
    dossier_medicale = models.ForeignKey(DossierMedicale, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()

    def __str__(self):
        return self.dossier_medicale.patient.username
class Disponibilite(models.Model):
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='disponibilites')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def __str__(self):
        return f"{self.medecin.username} : {self.date_debut} - {self.date_fin}"

class RendezVous(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, limit_choices_to={'is_doctor': False}, related_name='rendezvous_patient',null=True)
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='rendezvous_medecin')
    date = models.DateTimeField()
    raison = models.TextField(blank=True)

    def __str__(self):
        return f"Rendez-vous avec Dr. {self.medecin.username} le {self.date}"
