import sqlite3
import os

def check_db():
    db_path = 'data.db'
    print(f"Vérification de la base de données: {os.path.abspath(db_path)}")
    
    if not os.path.exists(db_path):
        print("ERREUR: Le fichier de base de données n'existe pas!")
        return
    
    print(f"Taille du fichier: {os.path.getsize(db_path)} octets")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Connexion à la base de données réussie!")
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("Aucune table trouvée dans la base de données.")
            return
            
        print("\nTables trouvées:")
        for table in tables:
            table_name = table[0]
            print(f"\n--- {table_name} ---")
            
            # Afficher les colonnes
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Colonnes:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Compter les lignes
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Nombre d'entrées: {count}")
            
            # Afficher un exemple de données si disponible
            if count > 0:
                print("\nExemple de données:")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                row = cursor.fetchone()
                print(row)
        
    except sqlite3.Error as e:
        print(f"ERREUR SQLite: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nConnexion à la base de données fermée.")

if __name__ == "__main__":
    check_db()
