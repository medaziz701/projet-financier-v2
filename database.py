import sqlite3
import os

def connecter():
    """Établit une connexion à la base de données"""
    return sqlite3.connect("data.db")

def initialiser_bdd():
    """Initialise toutes les tables nécessaires avec leurs relations"""
    conn = connecter()
    cur = conn.cursor()
    
    # Désactive temporairement les contraintes de clé étrangère
    cur.execute("PRAGMA foreign_keys = OFF")
    
    # Liste de toutes les tables à créer
    schemas = [
        """CREATE TABLE IF NOT EXISTS etablissement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT,
            code_postal TEXT,
            ville TEXT,
            pays TEXT DEFAULT 'Maroc',
            telephone TEXT,
            email TEXT,
            registre_commerce TEXT,
            identifiant_fiscal TEXT,
            cnss TEXT,
            ice TEXT,
            logo_path TEXT,
            date_creation TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role TEXT DEFAULT 'utilisateur'
        )""",
        """CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT,
            telephone TEXT,
            adresse TEXT,
            identifiant_fiscal TEXT,
            solde_credit REAL DEFAULT 0
        )""",
        
        """CREATE TABLE IF NOT EXISTS fournisseurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT,
            telephone TEXT,
            adresse TEXT
        )""",
        # Ajout de la table bon_livraison pour éviter l'erreur
        """CREATE TABLE IF NOT EXISTS bon_livraison (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            code_fournisseur TEXT,
            nom_fournisseur TEXT,
            id_produit INTEGER,
            nom_produit TEXT,
            quantite INTEGER,
            prix_unitaire REAL,
            remise REAL,
            total REAL
        )""",
        
        """CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit_id INTEGER,
            client_id INTEGER,
            quantite INTEGER,
            date TEXT,
            total REAL,
            FOREIGN KEY(produit_id) REFERENCES articles(code),
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )"""
    ]
    
    # Exécute tous les schémas de création
    for schema in schemas:
        try:
            cur.execute(schema)
        except sqlite3.Error as e:
            print(f"Erreur création table: {e}")
    
    # Réactive les contraintes de clé étrangère
    cur.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()

def creer_etablissement(nom, adresse, code_postal, ville, telephone, email, identifiant_fiscal="", logo_path=None, **kwargs):
    """Crée un nouvel établissement dans la base de données"""
    conn = connecter()
    cur = conn.cursor()
    try:
        # Supprimer d'abord tout enregistrement existant
        cur.execute("DELETE FROM etablissement")
        
        # Insérer le nouvel enregistrement
        cur.execute("""
            INSERT INTO etablissement (
                nom, adresse, code_postal, ville, telephone, email, 
                identifiant_fiscal, logo_path, date_creation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        """, (nom, adresse, code_postal, ville, telephone, email, 
              identifiant_fiscal, logo_path))
        
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de l'établissement: {e}")
        return None
    finally:
        conn.close()

def get_etablissement():
    """Récupère les informations de l'établissement sous forme de dict.
    Clés: id, nom, adresse, code_postal, ville, telephone, email, pays,
          date_creation, identifiant_fiscal, logo_path
    """
    conn = connecter()
    try:
        # Permet un accès par nom de colonne
        import sqlite3 as _sqlite3
        conn.row_factory = _sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                id, nom, adresse, code_postal, ville, telephone, email, 
                pays, date_creation, identifiant_fiscal, logo_path
            FROM etablissement 
            LIMIT 1
            """
        )
        row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'établissement: {e}")
        return None
    finally:
        conn.close()

def verifier_et_mettre_a_jour_schema():
    """Vérifie et met à jour le schéma de la base de données"""
    conn = connecter()
    cur = conn.cursor()
    
    try:
        # 1. Vérifie l'existence des tables principales
        tables_requises = {'clients', 'articles', 'fournisseurs', 'ventes'}
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_existantes = {row[0] for row in cur.fetchall()}
        
        if not tables_requises.issubset(tables_existantes):
            print("Tables manquantes, recréation de la base...")
            conn.close()
            os.remove("data.db")
            initialiser_bdd()
            return
        
        # 2. Vérifie et met à jour la table clients
        cur.execute("PRAGMA table_info(clients)")
        colonnes_clients = [col[1] for col in cur.fetchall()]
        for col in ('adresse', 'identifiant_fiscal', 'solde_credit'):
            if col not in colonnes_clients:
                print(f"Ajout de la colonne {col} à la table clients...")
                cur.execute(f"ALTER TABLE clients ADD COLUMN {col} TEXT")
        
        # 3. Vérifie et met à jour la table ventes
        cur.execute("PRAGMA table_info(ventes)")
        colonnes_ventes = [col[1] for col in cur.fetchall()]
        
        if 'total' not in colonnes_ventes:
            print("Ajout de la colonne total à la table ventes...")
            cur.execute("ALTER TABLE ventes ADD COLUMN total REAL")
            
            # Calcule les totaux pour les ventes existantes
            cur.execute("""
                UPDATE ventes 
                SET total = (
                    SELECT a.prix_vente * ventes.quantite 
                    FROM articles a 
                    WHERE a.code = ventes.produit_id
                )
                WHERE total IS NULL
            """)
            
            conn.commit()
            print("Mise à jour du schéma terminée")
            
    except sqlite3.Error as e:
        print(f"Erreur lors de la vérification: {e}")
    finally:
        conn.close()

# Initialisation au démarrage
if __name__ == "__main__":
    if not os.path.exists("data.db"):
        print("Création d'une nouvelle base de données...")
        initialiser_bdd()
    else:
        print("Vérification du schéma existant...")
        verifier_et_mettre_a_jour_schema()
