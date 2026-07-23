import sqlite3

def view_etablissement():
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer les informations de la table etablissement
        cursor.execute("SELECT * FROM etablissement LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            print("Informations de l'établissement:")
            print("-" * 50)
            for key in row.keys():
                print(f"{key}: {row[key] if row[key] is not None else 'NULL'}")
        else:
            print("Aucune information d'établissement trouvée.")
            
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    view_etablissement()
