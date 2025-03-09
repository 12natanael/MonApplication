from django.db import models
from datetime import date



class PlanComptable(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = "plancomptable"



    def __str__(self):
        return self.nom
    


class Compte(models.Model):
    TYPE_CHOICES = [
        ('Actif', 'Actif'),
        ('Passif', 'Passif'),
        ('Capitaux propres', 'Capitaux propres'),
    ]

    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    numero = models.CharField(max_length=50, unique=True)
    solde = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    plan_comptable = models.ForeignKey(PlanComptable, on_delete=models.CASCADE)


    class Meta:
        managed = True
        db_table = "compte"


    def __str__(self):
        return f"{self.nom} ({self.numero})"


class Ecriture(models.Model):
    date = models.DateField()
    montant = models.DecimalField(max_digits=18, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)
    justificatif = models.CharField(max_length=255, blank=True, null=True)
    debit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='debits')
    credit = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='credits')

    class Meta:
        managed = True
        db_table = "ecriture"


    def __str__(self):
        return f"Ecriture du {self.date} - {self.montant} €"


class Client(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    
    class Meta:
        managed = True
        db_table = "client"

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    
    class Meta:
        managed = True
        db_table = "fournisseur"

    def __str__(self):
        return self.nom


class Facture(models.Model):
    ETAT_CHOICES = [
        ('Non paye', 'Non payé'),
        ('Partiellement paye', 'Partiellement payé'),
        ('Paye', 'Payé'),
    ]

    numero = models.CharField(max_length=50)
    date_emission = models.DateField()
    date_echeance = models.DateField()
    montant_total = models.DecimalField(max_digits=18, decimal_places=2)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        managed = True
        db_table = "facture"


    def __str__(self):
        return f"Facture {self.numero}"


class Tresorerie(models.Model):
    FLUX_CHOICES = [
        ('Entrée', 'Entrée'),
        ('Sortie', 'Sortie'),
    ]

    date = models.DateField()
    flux = models.CharField(max_length=50, choices=FLUX_CHOICES)
    montant = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.TextField(blank=True, null=True)

   
    class Meta:
        managed = True
        db_table = "tresorerie"

    def __str__(self):
        return f"{self.flux} - {self.montant} € le {self.date}"


class Immobilisation(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_acquisition = models.DateField()
    valeur_acquisition = models.DecimalField(max_digits=18, decimal_places=2)
    duree_de_vie = models.IntegerField()
    taux_amortissement = models.DecimalField(max_digits=5, decimal_places=4)
    valeur_residuelle = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

   
    class Meta:
        managed = True
        db_table = "immobilisation"

    def __str__(self):
        return self.nom
    
