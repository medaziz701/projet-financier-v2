import sqlite3

def show_etablissement():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Récupérer la structure de la table
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Récupérer les données
        cursor.execute("SELECT * FROM etablissement")
        rows = cursor.fetchall()
        
        print("Contenu de la table 'etablissement':")
        print("-" * 50)
        
        # Afficher les noms des colonnes
        print(" | ".join(columns))
        print("-" * 50)
        
        # Afficher les données
        for row in rows:
            print(" | ".join(str(value) if value is not None else "NULL" for value in row))
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    show_etablissement()
