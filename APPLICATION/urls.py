from django.urls import path
from . import views 

urlpatterns = [
    path('',views.index,name = 'index'),
    path('creation-compte/', views.creation_compte, name='creation_compte'),
    path('enregistrer-compte/', views.enregistrer_compte, name='enregistrer_compte'),
    path('liste-comptes/', views.liste_comptes, name='liste_comptes'),
    path('modifier-compte/<int:compte_id>/', views.modifier_compte, name='modifier_compte'),
    path('supprimer-compte/<int:compte_id>/', views.supprimer_compte, name='supprimer_compte'),
    path('consulter-solde/<int:compte_id>/', views.consulter_solde, name='consulter_solde'),
    path('ajouter-ecriture/', views.ajouter_ecriture, name='ajouter_ecriture'),
    path('liste-ecritures/', views.liste_ecritures, name='liste_ecritures'),
    path('modifier-ecriture/<int:ecriture_id>/', views.modifier_ecriture, name='modifier_ecriture'),
    path('supprimer-ecriture/<int:ecriture_id>/', views.supprimer_ecriture, name='supprimer_ecriture'),
    # Clients
    path('liste-clients/', views.liste_clients, name='liste_clients'),
    path('ajouter-client/', views.ajouter_client, name='ajouter_client'),
    path('modifier-client/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('supprimer-client/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
    path('detail-client/<int:client_id>/', views.detail_client, name='detail_client'),

    # Fournisseurs
    path('liste-fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('ajouter-fournisseur/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('modifier-fournisseur/<int:fournisseur_id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer-fournisseur/<int:fournisseur_id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('detail-fournisseur/<int:fournisseur_id>/', views.detail_fournisseur, name='detail_fournisseur'),

    # Notifications
    path('notification/', views.notification, name='notification'),
    path('mes_factures/', views.mes_factures, name='mes_factures'),
     path('factures/creer/', views.creer_facture, name='creer_facture'),
    path('factures/<int:facture_id>/paiement/', views.enregistrer_paiement, name='enregistrer_paiement'),
]
    





