import sqlite3

def fix_etablissement_structure():
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la table etablissement existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etablissement'")
        if not cursor.fetchone():
            print("La table 'etablissement' n'existe pas.")
            return
            
        # Vérifier si la colonne identifiant_fiscal existe
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'identifiant_fiscal' not in columns:
            print("Ajout de la colonne 'identifiant_fiscal'...")
            cursor.execute("ALTER TABLE etablissement ADD COLUMN identifiant_fiscal TEXT")
            conn.commit()
            print("Colonne 'identifiant_fiscal' ajoutée avec succès.")
        
        # Afficher la structure actuelle
        print("\nStructure de la table 'etablissement':")
        cursor.execute("PRAGMA table_info(etablissement)")
        for col in cursor.fetchall():
            print(f"{col[1]} ({col[2]})")
        
        # Afficher les données actuelles
        print("\nDonnées actuelles:")
        cursor.execute("SELECT * FROM etablissement")
        for row in cursor.fetchall():
            print("\nEnregistrement:")
            for i, col in enumerate(cursor.description):
                print(f"{col[0]}: {row[i] if row[i] is not None else 'NULL'}")
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_etablissement_structure()
