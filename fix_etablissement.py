import sqlite3
import os

def main():
    print("Début de la vérification de la structure de la table 'etablissement'...")
    
    # Vérifier si le fichier de base de données existe
    if not os.path.exists('data.db'):
        print("ERREUR: Le fichier 'data.db' n'existe pas dans le répertoire courant.")
        print(f"Répertoire courant: {os.getcwd()}")
        return
    
    try:
        # Se connecter à la base de données
        print("Connexion à la base de données...")
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        print("Vérification de l'existence de la table 'etablissement'...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etablissement'")
        if not cursor.fetchone():
            print("La table 'etablissement' n'existe pas. Création en cours...")
            cursor.execute("""
                CREATE TABLE etablissement (
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
                )
            """)
            conn.commit()
            print("Table 'etablissement' créée avec succès.")
        else:
            print("La table 'etablissement' existe déjà.")
        
        # Vérifier si la colonne identifiant_fiscal existe
        print("\nVérification de la colonne 'identifiant_fiscal'...")
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'identifiant_fiscal' not in columns:
            print("La colonne 'identifiant_fiscal' n'existe pas. Ajout en cours...")
            cursor.execute("""
                ALTER TABLE etablissement 
                ADD COLUMN identifiant_fiscal TEXT
            """)
            conn.commit()
            print("Colonne 'identifiant_fiscal' ajoutée avec succès.")
        else:
            print("La colonne 'identifiant_fiscal' existe déjà.")
        
        # Afficher la structure actuelle
        print("\nStructure actuelle de la table 'etablissement':")
        cursor.execute("PRAGMA table_info(etablissement)")
        for col in cursor.fetchall():
            print(f"- {col[1]} ({col[2]})")
        
        # Vérifier les données existantes
        print("\nVérification des données existantes...")
        cursor.execute("SELECT * FROM etablissement")
        rows = cursor.fetchall()
        
        if not rows:
            print("Aucune donnée trouvée dans la table 'etablissement'.")
            print("Veuillez ajouter les informations de votre établissement via le menu de l'application.")
        else:
            print("\nDonnées actuelles dans la table 'etablissement':")
            cursor.execute("PRAGMA table_info(etablissement)")
            columns = [col[1] for col in cursor.fetchall()]
            
            for i, row in enumerate(rows, 1):
                print(f"\nEnregistrement {i}:")
                for col_name, value in zip(columns, row):
                    print(f"  {col_name}: {value if value is not None else 'NULL'}")
        
        print("\nVérification terminée avec succès!")
        
    except sqlite3.Error as e:
        print(f"\nERREUR SQLite: {e}")
    except Exception as e:
        print(f"\nERREUR: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
