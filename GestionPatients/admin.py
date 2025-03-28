from django.contrib import admin
from .models import User,DossierMedicale,RendezVous,Memo,Disponibilite

admin.site.register(User)
class AdminaDossierMedicale(admin.ModelAdmin):
    list_display=('medecin_responsable','notes','patient','antecedents_medicaux','medicaments_actuels','allergies','examens_complementaires','date_ouverture')
admin.site.register(DossierMedicale,AdminaDossierMedicale)
class AdminaMemo(admin.ModelAdmin):
    list_display=('dossier_medicale','date_creation','contenu')
admin.site.register(Memo,AdminaMemo)
class AdminaRendezVous(admin.ModelAdmin):
    list_display=('patient','medecin','raison','date')
admin.site.register(RendezVous)
class AdminaDisponibilite(admin.ModelAdmin):
    list_display=('medecin','date_debut','date_fin')
admin.site.register(Disponibilite)
# Register your models here.
