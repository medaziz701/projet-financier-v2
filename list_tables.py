import sqlite3

def lister_tables():
    """Liste toutes les tables de la base de données"""
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Récupère toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables existantes dans la base de données :")
        print("-" * 40)
        
        if tables:
            for i, table in enumerate(tables, 1):
                table_name = table[0]
                print(f"{i}. {table_name}")
                
                # Obtient le nombre d'enregistrements dans chaque table
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   → {count} enregistrement(s)")
                print()
        else:
            print("Aucune table trouvée dans la base de données.")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Erreur lors de l'accès à la base de données : {e}")

if __name__ == "__main__":
    lister_tables()
