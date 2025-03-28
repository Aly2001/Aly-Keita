from django.shortcuts import render,redirect,get_object_or_404
from GestionPatient import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from.models import User,Disponibilite,RendezVous
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.units import inch
from django.conf import settings
def pageaccueil(request,**kwargs):
    return render(request,'pageaccueil.html')
def inscription(request,**kwargs):
    if request.method=='POST':
        username=request.POST.get('username')
        username=username.upper()
        daten=request.POST.get('date_of_birth')
        email_address=request.POST.get('email_address')
        password1=request.POST.get('pw1')
        User = get_user_model()  
        try:
            user=User.objects.create(username=username,email=email_address,is_active=False,password=make_password(password1),date_naissance=daten)
            messages.success(request,"Compte créé avec succes !")

            subject="Creation de votre compte prise de rendez-vous Medicale"
            message="Bonjour "+username+"\nAvec plaisir de vous informer que votre compte a été creé avec succes !\n\n\nMerci coordialement !"
            from_email=settings.EMAIL_HOST_USER
            to_list=[user.email]
            send_mail(subject,message,from_email,to_list,fail_silently=False)
            #email de confirmation
            current_site=get_current_site(request)
            subject="Confirmation de l'adresse mail"
            message=render_to_string('emailconfirme.html',{
                "name":username,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generatorToken.make_token(user)
            })
            email=EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.fail_silently=False
            email.send()
            return redirect('connecter')
        except IntegrityError:
            messages.error(request,"Cet utilisateur existe dejà")
            return redirect('inscription')
    return render(request,'Inscription.html')
def connecter(request, **kwargs):
    if 'c' not in request.session:
        request.session['c'] = 0
    
    if request.method == 'POST':
        if 'username' in request.POST and 'pwc' in request.POST:
            username = request.POST['username']
            password = request.POST['pwc']
            username = username.upper()
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_active:
                login(request, user)
                
                if  user.is_doctor:
                    messages.success(request, "Connexion en tant que Médecin bien établie !")
                    return redirect('redirectpagedoctor')
                else:
                    messages.success(request, "Connexion en tant que Patient bien établie !")
                    return redirect('redirectpagePatient')
            
            elif user is not None and not user.is_active:
                messages.warning(request, "Votre compte n'est pas actif. Veuillez l'activer !")
                return redirect('inscription')
            
            else:
                request.session['c'] += 1
                if request.session['c'] >= 3:
                    request.session['c'] = 0
                    messages.error(request, "Ce compte n'existe pas. Veuillez créer votre compte.")
                    return redirect('inscription')
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    
    return render(request, 'Connecter.html')
def redirectpagedoctor(request ,**kwargs):
    return render (request,'pageDoctor.html')
def redirectpagePatient(request,**kwargs):
    return render (request,'pagePatient.html')
@login_required
def deconnecter(request,**kwargs):
    logout(request)
    return redirect(connecter)
def apropos(request,**kwargs):
    return render(request,'apropos.html')
@login_required
def listeDoctor(request,**kwargs):
    listeDoctor=User.objects.filter(is_doctor=True)
    contex={'listeDoctor':listeDoctor}
    return render(request,'listeDoctor.html',contex)
@login_required
def disponibilitesMedecin(request,my_id,**kwargs):
    doctor = get_object_or_404(User, id=my_id, is_doctor=True)
    disponibilit=Disponibilite.objects.filter(medecin=doctor).order_by('date_debut')
    contex={'disponibilite':disponibilit,'doctor':doctor}
    return render (request,'disponibilitesMedecin.html',contex)
@login_required
def medecincinPlaningRdv(request,**kwargs):
    user=request.user
    rdv=RendezVous.objects.filter(medecin=user)
    contex= {'rdv':rdv}
    return render(request,'medecincinPlaningRdv.html',contex)
@login_required
def planingallMedecin(request, **kwargs):
    rdv = RendezVous.objects.all()
    if request.method == 'GET':
        specialite = request.GET.get('specialite')
        if specialite:
            rdv = RendezVous.objects.filter(medecin__specialite__icontains=specialite)
    context = {'rdv': rdv}
    return render(request, 'planingallMedecin.html', context)
@login_required
def planingparticulierMedecin(request,my_id, **kwargs):
    user = User.objects.get(id=my_id)
    rdv = RendezVous.objects.filter(medecin=user)
    if request.method == 'GET':
        specialite = request.GET.get('specialite')
        if specialite:
            rdv = RendezVous.objects.filter(medecin__specialite__icontains=specialite)
    context = {'rdv': rdv}
    return render(request, 'planingaparticulierMedecin.html', context)

@login_required
def mesRendezVous(request,**kwargs):
    user=request.user
    rdv=RendezVous.objects.filter(patient=user)
    contex={'rdv':rdv}
    return render(request,'mesRendezVous.html',contex)
@login_required
def rendezVousConserver(request,**kwargs):
    user=request.user
    rdv=RendezVous.objects.filter(medecin=user,patient__isnull=False)
    contex={'rdv':rdv}
    return render(request,'rendezVousConserver.html',contex)
@login_required
def creerRebdezVous(request,**kwargs):
    user=request.user
    contex={'rdv':user}
    if request.method=='POST':
        date=request.POST.get('date')
        heure=request.POST.get('heure')
        date_heure_str = f"{date} {heure}"
        date_heure = datetime.datetime.strptime(date_heure_str, '%Y-%m-%d %H:%M')
        rdv = RendezVous.objects.create(medecin=user, date=date_heure)
        messages.success(request,"Rendez-vous creé avec succes !")
        return redirect(medecincinPlaningRdv)

    return render(request,'creerRendezVous.html',contex)
@login_required
def reserverRendezVous(request, my_id, **kwargs):
    rdv = get_object_or_404(RendezVous, id=my_id)
    if request.method == 'POST':
        if rdv.patient is not None:
            messages.error(request, "Ce planning est déjà réservé !")
            return redirect(reverse('planingallMedecin'))  # Assurez-vous que 'planingallMedecin' est le nom de l'URL
        else:
            user = request.user
            motif = request.POST.get('motif')
            if motif:  # Vérifie que le motif n'est pas vide
                rdv.patient = user
                rdv.raison = motif
                rdv.save()
                
                subject = "Confirmation de prise de rendez-vous"
                message = (
                    f"Bonjour {rdv.patient.username},\n\n"
                    "Nous sommes ravis de vous confirmer votre rendez-vous médical.\n"
                    "Vous trouverez en pièce jointe la confirmation de votre rendez-vous médical,que vous êtes prié(e) d'imprimer et de présenter le jour de votre consultation à l'accueil de l'hôpital Mohammed VI.\n"

                    "Cordialement.\n"
                    
                )
                from_email = settings.EMAIL_HOST_USER
                to_email = [rdv.patient.email]

                pdf_buffer = generate_pdf(rdv)

                email = EmailMessage(
                    subject,
                    message,
                    from_email,
                    to_email,
                )

                email.attach(f'confirmation_rdv_{rdv.patient.username}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                email.send()
                messages.success(request, "Rendez-vous a été bien réservé !")
                return redirect(reverse('mesRendezVous'))  # Assurez-vous que 'mesRendezVous' est le nom de l'URL
            else:
                messages.error(request, "Le motif du rendez-vous est requis.")
                return render(request, 'motifrdv.html', {'rdv': rdv})
    return render(request, 'motifrdv.html', {'rdv': rdv})
def generate_pdf(rdv):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Définition de la police et de la taille du texte
    p.setFont("Times-Roman", 13)

    message = (
    f"Bonjour {rdv.patient.username},\n\n"
    f"Nous vous confirmons votre rendez-vous avec le Dr. {rdv.medecin.username} pour le motif suivant :\n {rdv.raison}.\n\n"
    f"Votre rendez-vous est prévu le {rdv.date.strftime('%d/%m/%Y')} à {rdv.date.strftime('%H:%M')}.\n\n"
    "Il est impératif que vous vous présentiez à l'accueil de l'Hôpital Mohammed VI\n avec ce fichier imprimé. "
    "Sans ce document, l'accès à votre rendez-vous ne vous sera pas autorisé.\n\n"
    "En cas d'imprévu ou d'annulation, veuillez nous en informer au moins un jour à l'avance.\n\n"
    "Nous restons à votre disposition pour toute question supplémentaire.\n\n"
    "Cordialement,\n"
    f"L'équipe du Dr. {rdv.medecin.username}\n"
    "Hôpital Mohammed VI"
)
    
    # Ajout du contenu au PDF avec un positionnement amélioré
    text_object = p.beginText(1 * inch, height - 1 * inch)
    for line in message.split("\n"):
        text_object.textLine(line)
    
    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
@login_required
def annulerRendezVous(request,my_id,**kwargs):
    user=request.user
    rdv=get_object_or_404(RendezVous,id=my_id,patient=user)
    rdv.patient=None
    rdv.save()
    messages.success(request,"Rendez a été bien annulé !")
    return redirect(mesRendezVous)
@login_required
def delete_rendezvous(request,my_id,**kwargs):
    rdv=get_object_or_404(RendezVous,id=my_id,medecin=request.user)
    if rdv.patient:
        messages.success(request,"Impossible de Supprimer Planing car il est dejà reservé !")
        return redirect(reverse('medecincinPlaningRdv'))
    else:
        rdv.delete()
        messages.success(request,"Planing est Supprimé !")
        return redirect(reverse('medecincinPlaningRdv'))
@login_required        
def modify_rendezvous(request,my_id,**kwargs):
    rdv=get_object_or_404(RendezVous,id=my_id,medecin=request.user)
    if request.method=='POST':
        if rdv.patient:
            messages.success(request,"Ce Planing est dejà reservé par un patient !")
            return redirect(reverse('medecincinPlaningRdv'))
        else:
            date=request.POST.get('date')
            rdv.date=date
            rdv.save()
            messages.success(request,"Mis en jour de planing !")
            return redirect(reverse('medecincinPlaningRdv'))
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoeNotExist):
        user=None
    if user is not None and generatorToken.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Votre compte a été bien active !")
        return redirect(connecter)
    else:
        messages.error(request,"Activation du compte a echoué !")
        return redirect(pageaccueil)
@login_required
def annulerRendezVousMedecin(request,my_id,**kwargs):
    
    rdv=get_object_or_404(RendezVous,id=my_id)
    user=rdv.patient
    medecin=rdv.medecin
    rdv.patient=None
    rdv.save()
    subject = "Annulation de Votre Rendez-vous Médical"
    message = (
    "Bonjour " + user.username + "\n"
    "Nous vous informons que, malheureusement, votre rendez-vous prévu avec le Dr. " 
    + medecin.username + " le "+rdv.date.strftime('%d/%m/%Y')+" à "+rdv.date.strftime('%H:%M')+" doit être annulé en raison de circonstances imprévues.\n"
    "Nous nous excusons pour tout inconvénient que cela pourrait causer. Nous vous invitons à reprogrammer votre rendez-vous à une date ultérieure. "
    "Vous pouvez  visiter notre site web pour choisir un nouveau Rendez-vous.\n"
    "Merci de votre compréhension et de votre patience. Nous restons à votre disposition pour toute question ou assistance supplémentaire.\n\n"
    "Cordialement,\n"
    "Hopital Mohammmed VI\n"
    
    )
    from_email=settings.EMAIL_HOST_USER
    to_list=[user.email]
    send_mail(subject,message,from_email,to_list,fail_silently=False)
    messages.success(request,"Rendez a été bien annulé !")
    return redirect(rendezVousConserver)
    










    
# Create your views here.
