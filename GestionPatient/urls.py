"""
URL configuration for GestionPatient project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from GestionPatients import views
from GestionPatients.views import activate,generate_pdf,delete_rendezvous,annulerRendezVous,reserverRendezVous,apropos,creerRebdezVous,rendezVousConserver,mesRendezVous,medecincinPlaningRdv,planingallMedecin,deconnecter,disponibilitesMedecin,listeDoctor,pageaccueil,inscription,connecter,redirectpagedoctor,redirectpagePatient
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',pageaccueil,name='pageaccueil'),
    path('inscription',inscription,name='inscription'),
    path('connecter',connecter,name='connecter'),
    path('deconnecter',deconnecter,name='deconnecter'),
    path('redirectpagedoctor',redirectpagedoctor,name='redirectpagedoctor'),
    path('redirectpagePatient',redirectpagePatient,name='redirectpagePatient'),
    path('listeDoctor',listeDoctor,name='listeDoctor'),
    path('disponibilitesMedecin/<int:my_id>/',disponibilitesMedecin,name='disponibilitesMedecin'),
    path('medecincinPlaningRdv',medecincinPlaningRdv,name='medecincinPlaningRdv'),
    path('planingallMedecin',planingallMedecin,name='planingallMedecin'),
    path('mesRendezVous',mesRendezVous,name='mesRendezVous'),
    path('rendezVousConserver',rendezVousConserver,name='rendezVousConserver'),
    path('creerRebdezVous',creerRebdezVous,name='creerRebdezVous'),
    path('apropos',apropos,name='apropos'),
    path('reserverRendezVous/<int:my_id>',reserverRendezVous,name='reserverRendezVous'),
    path('annulerRendezVous/<int:my_id>',annulerRendezVous,name='annulerRendezVous'),
    path('delete_rendezvous/<int:my_id>/',delete_rendezvous,name='delete_rendezvous'),
    path('modify_rendezvous/<int:my_id>/',views.modify_rendezvous,name='modify_rendezvous'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    path('annulerRendezVousMedecin/<int:my_id>/',views.annulerRendezVousMedecin,name='annulerRendezVousMedecin'),
    path('planingparticulierMedecin/<int:my_id>/',views.planingparticulierMedecin,name='planingparticulierMedecin'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
