import sqlite3

def check_etablissement_structure():
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la table etablissement existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etablissement'")
        if not cursor.fetchone():
            print("La table 'etablissement' n'existe pas dans la base de données.")
            return
        
        # Vérifier la structure de la table
        print("\nStructure de la table 'etablissement':")
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = cursor.fetchall()
        
        # Afficher les colonnes
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        # Vérifier si la colonne identifiant_fiscal existe
        has_identifiant_fiscal = any(col[1] == 'identifiant_fiscal' for col in columns)
        
        if not has_identifiant_fiscal:
            print("\nLa colonne 'identifiant_fiscal' n'existe pas. Ajout en cours...")
            try:
                cursor.execute("""
                    ALTER TABLE etablissement 
                    ADD COLUMN identifiant_fiscal TEXT
                """)
                conn.commit()
                print("La colonne 'identifiant_fiscal' a été ajoutée avec succès.")
            except sqlite3.Error as e:
                print(f"Erreur lors de l'ajout de la colonne: {e}")
        else:
            print("\nLa colonne 'identifiant_fiscal' existe déjà dans la table.")
        
        # Afficher les données actuelles
        print("\nDonnées actuelles dans la table 'etablissement':")
        cursor.execute("SELECT * FROM etablissement")
        rows = cursor.fetchall()
        
        if not rows:
            print("Aucune donnée trouvée dans la table 'etablissement'.")
        else:
            print("\nEnregistrement actuel:")
            for i, col in enumerate(columns):
                print(f"{col[1]}: {rows[0][i] if rows[0][i] is not None else 'NULL'}")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_etablissement_structure()
