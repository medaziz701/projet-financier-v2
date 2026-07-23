import sqlite3

def check_etablissement():
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la table etablissement existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etablissement'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("La table 'etablissement' n'existe pas dans la base de données.")
            return
            
        # Afficher la structure de la table
        print("\nStructure de la table 'etablissement':")
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = cursor.fetchall()
        print("Colonnes:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        # Afficher les données de la table
        print("\nDonnées dans la table 'etablissement':")
        cursor.execute("SELECT * FROM etablissement")
        rows = cursor.fetchall()
        
        if not rows:
            print("Aucune donnée trouvée dans la table 'etablissement'.")
        else:
            for row in rows:
                print("\nEnregistrement:")
                for i, col in enumerate(columns):
                    print(f"{col[1]}: {row[i] if row[i] is not None else 'NULL'}")
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_etablissement()
