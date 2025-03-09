from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Compte, PlanComptable, Ecriture, Client, Fournisseur,Facture
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings


def index(request): 
    context = {"message": "hello word !"}
    template = loader.get_template("APPLICATION/index.html")
    return HttpResponse(template.render(context,request))




def creation_compte(request):
    plans_comptables = PlanComptable.objects.all()  
    return render(request, 'APPLICATION/creation_compte.html', {'plans_comptables': plans_comptables})


def enregistrer_compte(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        type_compte = request.POST.get('type')
        numero = request.POST.get('numero')
        solde = request.POST.get('solde')
        plan_comptable_id = request.POST.get('plan_comptable')

        
        if not nom or not type_compte or not numero or not solde or not plan_comptable_id:
            messages.error(request, 'Tous les champs sont obligatoires.')
            return redirect('creation_compte')

        try:
            solde = float(solde)  
        except ValueError:
            messages.error(request, 'Le solde doit être un nombre valide.')
            return redirect('creation_compte')

        try:
            plan_comptable = PlanComptable.objects.get(id=plan_comptable_id)
        except PlanComptable.DoesNotExist:
            messages.error(request, 'Plan comptable invalide.')
            return redirect('creation_compte')

        
        try:
            compte = Compte(
                nom=nom,
                type=type_compte,
                numero=numero,
                solde=solde,
                plan_comptable=plan_comptable
            )
            compte.save()
            messages.success(request, 'Compte enregistré avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement du compte: {str(e)}')

        return redirect('creation_compte')
    


def liste_comptes(request):
    
    comptes = Compte.objects.all()

    
    query = request.GET.get('q')
    if query:
        comptes = comptes.filter(nom__icontains=query)

    return render(request, 'APPLICATION/liste_comptes.html', {'comptes': comptes})



def modifier_compte(request, compte_id):
    compte = get_object_or_404(Compte, id=compte_id)
    if request.method == 'POST':
       
        compte.nom = request.POST.get('nom')
        compte.type = request.POST.get('type')
        compte.numero = request.POST.get('numero')
        compte.solde = request.POST.get('solde')
        compte.plan_comptable_id = request.POST.get('plan_comptable')
        compte.save()
        messages.success(request, 'Compte modifié avec succès!')
        return redirect('liste_comptes')
    return render(request, 'APPLICATION/modifier_compte.html', {'compte': compte})

def supprimer_compte(request, compte_id):
    compte = get_object_or_404(Compte, id=compte_id)
    compte.delete()
    messages.success(request, 'Compte supprimé avec succès!')
    return redirect('liste_comptes')

def consulter_solde(request, compte_id):
    compte = get_object_or_404(Compte, id=compte_id)
    return render(request, 'APPLICATION/consulter_solde.html', {'compte': compte})


def ajouter_ecriture(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        montant = request.POST.get('montant')
        commentaire = request.POST.get('commentaire')
        justificatif = request.POST.get('justificatif')
        debit_id = request.POST.get('debit')
        credit_id = request.POST.get('credit')

        
        if not date or not montant or not debit_id or not credit_id:
            messages.error(request, 'Tous les champs obligatoires doivent être remplis.')
            return redirect('ajouter_ecriture')

        try:
            montant = float(montant)  
        except ValueError:
            messages.error(request, 'Le montant doit être un nombre valide.')
            return redirect('ajouter_ecriture')

        try:
            debit = Compte.objects.get(id=debit_id)
            credit = Compte.objects.get(id=credit_id)
        except Compte.DoesNotExist:
            messages.error(request, 'Compte de débit ou crédit invalide.')
            return redirect('ajouter_ecriture')

        
        try:
            ecriture = Ecriture(
                date=date,
                montant=montant,
                commentaire=commentaire,
                justificatif=justificatif,
                debit=debit,
                credit=credit
            )
            ecriture.save()
            messages.success(request, 'Écriture enregistrée avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement de l\'écriture: {str(e)}')

        return redirect('ajouter_ecriture')

    
    comptes = Compte.objects.all()
    return render(request, 'APPLICATION/ajouter_ecriture.html', {'comptes': comptes})


def liste_ecritures(request):
    
    ecritures = Ecriture.objects.select_related('debit', 'credit').all()

    
    query = request.GET.get('q')
    if query:
        ecritures = ecritures.filter(
            Q(date__icontains=query) |
            Q(montant__icontains=query) |
            Q(commentaire__icontains=query) |
            Q(debit__nom__icontains=query) |
            Q(credit__nom__icontains=query)
        )

    return render(request, 'APPLICATION/liste_ecritures.html', {'ecritures': ecritures})

def modifier_ecriture(request, ecriture_id):
    ecriture = get_object_or_404(Ecriture, id=ecriture_id)
    if request.method == 'POST':
        
        ecriture.date = request.POST.get('date')
        ecriture.montant = request.POST.get('montant')
        ecriture.commentaire = request.POST.get('commentaire')
        ecriture.justificatif = request.POST.get('justificatif')
        ecriture.debit_id = request.POST.get('debit')
        ecriture.credit_id = request.POST.get('credit')
        ecriture.save()
        messages.success(request, 'Écriture modifiée avec succès!')
        return redirect('liste_ecritures')
    
    
    comptes = Compte.objects.all()
    return render(request, 'APPLICATION/modifier_ecriture.html', {'ecriture': ecriture, 'comptes': comptes})

def supprimer_ecriture(request, ecriture_id):
    ecriture = get_object_or_404(Ecriture, id=ecriture_id)
    ecriture.delete()
    messages.success(request, 'Écriture supprimée avec succès!')
    return redirect('liste_ecritures')




def liste_clients(request):
    clients = Client.objects.all()
    query = request.GET.get('q')
    if query:
        clients = clients.filter(
            Q(nom__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query)
        )
    return render(request, 'APPLICATION/liste_clients.html', {'clients': clients})

def ajouter_client(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        try:
            Client.objects.create(nom=nom, adresse=adresse, email=email, telephone=telephone)
            messages.success(request, 'Client ajouté avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout du client: {str(e)}')

        return redirect('liste_clients')
    return render(request, 'APPLICATION/ajouter_client.html')

def modifier_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.nom = request.POST.get('nom')
        client.adresse = request.POST.get('adresse')
        client.email = request.POST.get('email')
        client.telephone = request.POST.get('telephone')
        client.save()
        messages.success(request, 'Client modifié avec succès!')
        return redirect('liste_clients')
    return render(request, 'APPLICATION/modifier_client.html', {'client': client})

def supprimer_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    messages.success(request, 'Client supprimé avec succès!')
    return redirect('liste_clients')

def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
     
    transactions = []  
    return render(request, 'APPLICATION/detail_client.html', {'client': client, 'transactions': transactions})


def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    query = request.GET.get('q')
    if query:
        fournisseurs = fournisseurs.filter(
            Q(nom__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query)
        )
    return render(request, 'APPLICATION/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

def ajouter_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        try:
            Fournisseur.objects.create(nom=nom, adresse=adresse, email=email, telephone=telephone)
            messages.success(request, 'Fournisseur ajouté avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout du fournisseur: {str(e)}')

        return redirect('liste_fournisseurs')
    return render(request, 'APPLICATION/ajouter_fournisseur.html')

def modifier_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom')
        fournisseur.adresse = request.POST.get('adresse')
        fournisseur.email = request.POST.get('email')
        fournisseur.telephone = request.POST.get('telephone')
        fournisseur.save()
        messages.success(request, 'Fournisseur modifié avec succès!')
        return redirect('liste_fournisseurs')
    return render(request, 'APPLICATION/modifier_fournisseur.html', {'fournisseur': fournisseur})

def supprimer_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    fournisseur.delete()
    messages.success(request, 'Fournisseur supprimé avec succès!')
    return redirect('liste_fournisseurs')

def detail_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    
    transactions = []  
    return render(request, 'APPLICATION/detail_fournisseur.html', {'fournisseur': fournisseur, 'transactions': transactions})


def notification(request):
    
    factures_en_retard = Facture.objects.filter(date_echeance__lt=now().date(), etat='Non paye')
    return  render(request, 'APPLICATION/notification.html', {'factures_en_retard': factures_en_retard})


def mes_factures(request):
    factures = Facture.objects.all()
    return render(request, 'APPLICATION/mes_factures.html', {'factures': factures})


def creer_facture(request):
    if request.method == "POST":
        numero = request.POST['numero']
        date_emission = request.POST['date_emission']
        date_echeance = request.POST['date_echeance']
        montant_total = request.POST['montant_total']
        etat = request.POST['etat']
        client_id = request.POST['client']
        client = Client.objects.get(id=client_id)

        facture = Facture.objects.create(
            numero=numero,
            date_emission=date_emission,
            date_echeance=date_echeance,
            montant_total=montant_total,
            etat=etat,
            client=client
        )

        
        if client.email:
            send_mail(
                subject=f'Facture {facture.numero}',
                message=f'Bonjour {client.nom},\n\nVotre facture {facture.numero} a été créée.',
                from_email='ton_email@exemple.com',
                recipient_list=[client.email],
            )

        messages.success(request, "Facture créée avec succès et envoyée au client.")
        return redirect('mes_factures')

    clients = Client.objects.all()
    return render(request, 'APPLICATION/creer_facture.html', {'clients': clients})


def enregistrer_paiement(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    if request.method == "POST":
        montant_paye = float(request.POST['montant_paye'])
        reste = float(facture.montant_total) - montant_paye

        if reste <= 0:
            facture.etat = "Paye"
        else:
            facture.etat = "Partiellement paye"

        facture.save()
        messages.success(request, f"Paiement enregistré. Solde restant : {reste:.2f} €")
        return redirect('mes_factures')

    return render(request, 'APPLICATION/enregistrer_paiement.html', {'facture': facture})


