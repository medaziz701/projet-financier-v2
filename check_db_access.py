import sqlite3
import os

def check_database():
    db_file = 'data.db'
    
    # Vérifier si le fichier existe
    if not os.path.exists(db_file):
        print(f"Le fichier {db_file} n'existe pas dans le répertoire courant.")
        return
    
    # Vérifier les permissions du fichier
    print(f"Taille du fichier: {os.path.getsize(db_file)} octets")
    print(f"Droits d'accès: {oct(os.stat(db_file).st_mode)[-3:]}")
    
    try:
        # Essayer de se connecter à la base de données
        print("\nTentative de connexion à la base de données...")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Vérifier si la table etablissement existe
        print("\nVérification des tables...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables trouvées: {len(tables)}")
        for table in tables:
            print(f"- {table[0]}")
        
        # Vérifier la structure de la table etablissement
        if any('etablissement' in table for table in tables):
            print("\nStructure de la table 'etablissement':")
            cursor.execute("PRAGMA table_info(etablissement)")
            for col in cursor.fetchall():
                print(f"- {col[1]} ({col[2]})")
            
            # Afficher les données de la table etablissement
            print("\nDonnées dans 'etablissement':")
            cursor.execute("SELECT * FROM etablissement")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Aucune donnée trouvée dans la table 'etablissement'.")
        
        print("\nTest de connexion réussi!")
        
    except sqlite3.Error as e:
        print(f"\nErreur SQLite: {e}")
    except Exception as e:
        print(f"\nErreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    check_database()
