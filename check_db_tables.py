import sqlite3
import os

def check_tables():
    db_path = 'data.db'
    print(f"Vérification du fichier: {os.path.abspath(db_path)}")
    print(f"Taille: {os.path.getsize(db_path) if os.path.exists(db_path) else 'Fichier introuvable'} octets")
    
    if not os.path.exists(db_path):
        print("ERREUR: Le fichier de base de données n'existe pas!")
        return
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("Aucune table trouvée dans la base de données!")
            return
            
        print("\nTables trouvées:")
        for table in tables:
            table_name = table[0]
            print(f"\n--- {table_name} ---")
            
            # Nombre de lignes
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"Lignes: {count}")
                
                # Aperçu des colonnes
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print("Colonnes:", ", ".join([col[1] for col in columns]))
                
                # Aperçu des données
                if count > 0:
                    print("Première ligne:")
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                    print(cursor.fetchone())
            except sqlite3.Error as e:
                print(f"Erreur lors de la lecture de la table {table_name}: {e}")
                
    except sqlite3.Error as e:
        print(f"ERREUR SQLite: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_tables()
