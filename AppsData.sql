-- Database: AppsData

-- DROP DATABASE IF EXISTS "AppsData";

CREATE DATABASE "AppsData"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'fr-FR'
    LC_CTYPE = 'fr-FR'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


	CREATE TABLE PlanComptable ( 
id SERIAL PRIMARY KEY, 
nom VARCHAR(255) NOT NULL UNIQUE, 
description TEXT 
); 

CREATE TABLE Compte ( 
id SERIAL PRIMARY KEY,
nom VARCHAR(255) NOT NULL,  
type VARCHAR(50) NOT NULL CHECK (type IN ('Actif', 'Passif', 'Capitaux propres')), 
numero VARCHAR(50) NOT NULL UNIQUE,
solde DECIMAL(18, 2) NOT NULL DEFAULT 0 CHECK (solde >= 0), 
plan_comptable_id INT NOT NULL, 
FOREIGN KEY (plan_comptable_id) REFERENCES PlanComptable(id) ON DELETE CASCADE 
);

CREATE TABLE Ecriture ( 
id SERIAL PRIMARY KEY, 
date DATE NOT NULL CHECK (date <= CURRENT_DATE), 
montant DECIMAL(18, 2) NOT NULL CHECK (montant > 0), 
commentaire TEXT, 
justificatif VARCHAR(255), 
debit_id INT NOT NULL, 
credit_id INT NOT NULL, 
FOREIGN KEY (debit_id) REFERENCES Compte(id) ON DELETE CASCADE, 
FOREIGN KEY (credit_id) REFERENCES Compte(id) ON DELETE CASCADE
); 

CREATE TABLE Client ( 
id SERIAL PRIMARY KEY, 
nom VARCHAR(255) NOT NULL,  
adresse TEXT,  
email VARCHAR(255) UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'), 
telephone VARCHAR(50) 
);

CREATE TABLE Fournisseur ( 
id SERIAL PRIMARY KEY, 
nom VARCHAR(255) NOT NULL, 
adresse TEXT,  
email VARCHAR(255) UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'), 
telephone VARCHAR(50) 
); 

CREATE TABLE Facture ( 
id SERIAL PRIMARY KEY, 
numero VARCHAR(50) NOT NULL,  
date_emission DATE NOT NULL CHECK (date_emission <= CURRENT_DATE),  
date_echeance DATE NOT NULL CHECK (date_echeance >= date_emission), 
montant_total DECIMAL(18, 2) NOT NULL CHECK (montant_total >= 0), 
etat VARCHAR(50) NOT NULL CHECK (etat IN ('Non paye', 'Partiellement paye', 'Paye')),
client_id INT , 
fournisseur_id INT, 
FOREIGN KEY (client_id) REFERENCES Client(id) ON DELETE SET NULL, 
FOREIGN KEY (fournisseur_id) REFERENCES Fournisseur(id) ON DELETE SET NULL 
);

CREATE TABLE Tresorerie ( 
id SERIAL PRIMARY KEY, 
date DATE NOT NULL CHECK (date <= CURRENT_DATE),  
flux VARCHAR(50) NOT NULL CHECK (flux IN ('Entrée', 'Sortie')),
montant DECIMAL(18, 2) NOT NULL CHECK (montant > 0),  
description TEXT 
);

CREATE TABLE Immobilisation ( 
id SERIAL PRIMARY KEY, 
nom VARCHAR(255) NOT NULL, 
description TEXT, 
date_acquisition DATE NOT NULL CHECK (date_acquisition <= CURRENT_DATE), 
valeur_acquisition DECIMAL(18, 2) NOT NULL CHECK (valeur_acquisition >= 0), 
duree_de_vie INT NOT NULL CHECK (duree_de_vie > 0), 
taux_amortissement DECIMAL(5, 4) NOT NULL CHECK (taux_amortissement BETWEEN 0 AND 1), 
valeur_residuelle DECIMAL(18, 2) CHECK (valeur_residuelle >= 0)  -- Assure-toi de ne pas inclure de caractères invisibles ici
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'; 

INSERT INTO PlanComptable (nom, description) VALUES 
('Plan Comptable Général', 'Plan comptable standard pour entreprises.'), 
('Plan Comptable Simplifié', 'Plan comptable pour les petites entreprises.'), 
('Plan Comptable Avancé', 'Plan comptable pour les grandes entreprises.'), 
('Plan Comptable Associatif', 'Plan comptable pour associations.'), 
('Plan Comptable Bancaire', 'Plan comptable spécifique au secteur bancaire.'); 

INSERT INTO Compte (nom, type, numero, solde, plan_comptable_id) VALUES 
('Caisse', 'Actif', '1000', 15000.00, 1), 
('Banque', 'Actif', '1001', 50000.00, 1), 
('Capital Social', 'Capitaux propres', '3000', 100000.00, 1), 
('Dettes Fournisseurs', 'Passif', '2000', 25000.00, 1), 
('Immobilisations Corporelles', 'Actif', '4000', 75000.00, 1);  

DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 6..100 LOOP 
        INSERT INTO Compte (nom, type, numero, solde, plan_comptable_id) 
        VALUES ( 
            'Compte ' || i,  
            CASE 
                WHEN i % 3 = 0 THEN 'Actif' 
                WHEN i % 3 = 1 THEN 'Passif' 
                ELSE 'Capitaux propres' 
            END, 
            '10' || i, 
            ROUND((RANDOM() * 10000)::NUMERIC, 2),  -- Applique une conversion explicite
            1  -- Plan comptable ID
        ); 
    END LOOP; 
END $$;

DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Ecriture (date, montant, commentaire, debit_id, credit_id) 
        VALUES ( 
            CURRENT_DATE - (i * INTERVAL '1 day'), 
            ROUND((RANDOM() * 5000 + 100)::NUMERIC, 2), 
            'Ecriture automatique ' || i, 
            (SELECT id FROM Compte ORDER BY RANDOM() LIMIT 1),  -- Récupère un ID aléatoire de la table Compte
            (SELECT id FROM Compte ORDER BY RANDOM() LIMIT 1)   -- Récupère un autre ID aléatoire de la table Compte
        ); 
    END LOOP; 
END $$;

DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Client (nom, adresse, email, telephone) 
        VALUES ( 
            'Client ' || i, 
            'Adresse ' || i, 
            'client' || i || '@example.com', 
           '6' || i || '0000000' 
        ); 
    END LOOP; 
END $$;


DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Fournisseur (nom, adresse, email, telephone) 
        VALUES ( 
            'Fournisseur ' || i, 
            'Adresse ' || i, 
            'fournisseur' || i || '@example.com', 
            '7' || i || '0000000' 
        ); 
    END LOOP; 
END $$;


DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Tresorerie (date, flux, montant, description) 
        VALUES ( 
            CURRENT_DATE - (i * INTERVAL '1 day'), 
            CASE WHEN i % 2 = 0 THEN 'Entrée' ELSE 'Sortie' END, 
            ROUND((RANDOM() * 3000 + 500)::NUMERIC, 2), 
            'Transaction ' || i 
        ); 
    END LOOP; 
END $$; 

DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Immobilisation (nom, description, date_acquisition, valeur_acquisition, duree_de_vie, 
        taux_amortissement, valeur_residuelle) 
        VALUES ( 
            'Immobilisation ' || i, 
            'Description de l''immobilisation ' || i, 
            CURRENT_DATE - ((i * 30) * INTERVAL '1 day'), 
            ROUND((RANDOM() * 10000 + 1000)::NUMERIC, 2),  -- Conversion explicite en NUMERIC
            (i % 10) + 1, 
            ROUND(RANDOM()::NUMERIC, 4),  -- Conversion en NUMERIC
            ROUND((RANDOM() * 500)::NUMERIC, 2)  -- Conversion en NUMERIC
        );
    END LOOP; 
END $$;



DO $$ 
DECLARE 
    i INT; 
BEGIN 
    FOR i IN 1..100 LOOP 
        INSERT INTO Facture (numero, date_emission, date_echeance, montant_total, etat, client_id, 
fournisseur_id) 
        VALUES ( 
            'F' || LPAD(i::TEXT, 3, '0'), 
            CURRENT_DATE - (i * INTERVAL '1 day'), 
            CURRENT_DATE + ((i % 10) * INTERVAL '1 day'), 
            ROUND((RANDOM() * 1000 + 500)::NUMERIC, 2),
			 CASE WHEN i % 3 = 0 THEN 'Non paye' WHEN i % 3 = 1 THEN 'Partiellement paye' ELSE 'Paye' END, 
            (i % 20) + 1, 
            ((i + 5) % 20) + 1 
        ); 
    END LOOP; 
END $$; 





