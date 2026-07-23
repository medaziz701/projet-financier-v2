import sqlite3

def list_fournisseurs():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fournisseurs'")
        if not cursor.fetchone():
            print("La table 'fournisseurs' n'existe pas dans la base de données.")
            return
            
        # Compter les fournisseurs
        cursor.execute("SELECT COUNT(*) FROM fournisseurs")
        count = cursor.fetchone()[0]
        print(f"\nNombre total de fournisseurs: {count}")
        
        # Afficher les fournisseurs
        if count > 0:
            print("\nListe des fournisseurs:")
            cursor.execute("SELECT id, nom, email, telephone FROM fournisseurs")
            for row in cursor.fetchall():
                print(f"ID: {row[0]}, Nom: {row[1]}, Email: {row[2]}, Téléphone: {row[3]}")
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    list_fournisseurs()
