from django.contrib import admin
from .models import (
    PlanComptable, Compte, Ecriture,
    Client, Fournisseur, Facture,
    Tresorerie, Immobilisation,
)


class PlanComptableAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'description')

class CompteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'type', 'numero', 'solde', 'plan_comptable')

class EcritureAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'montant', 'debit', 'credit', 'commentaire')

class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'email', 'telephone')

class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'date_emission', 'date_echeance', 'montant_total', 'etat')

class TresorerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'flux', 'montant', 'description')

class ImmobilisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date_acquisition', 'valeur_acquisition', 'duree_de_vie')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','nom','adresse','email','telephone')





admin.site.register(PlanComptable,PlanComptableAdmin)
admin.site.register(Compte,CompteAdmin)
admin.site.register(Ecriture,EcritureAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Fournisseur,FournisseurAdmin)
admin.site.register(Facture,FactureAdmin)
admin.site.register(Tresorerie,TresorerieAdmin)
admin.site.register(Immobilisation,ImmobilisationAdmin)

