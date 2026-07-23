import os
import sqlite3

def main():
    db_path = 'data.db'
    print(f"Vérification de la base de données: {os.path.abspath(db_path)}")
    
    if not os.path.exists(db_path):
        print("ERREUR: Le fichier de base de données n'existe pas!")
        return
    
    print(f"Taille du fichier: {os.path.getsize(db_path)} octets")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
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
            
            # Compter les lignes
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Lignes: {count}")
            
            # Afficher les colonnes
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print("Colonnes:", ", ".join(columns))
            
            # Afficher un exemple de données si disponible
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                print("Exemple de données:", cursor.fetchone())
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
