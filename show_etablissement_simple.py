import sqlite3

def show_etablissement():
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        
        # Créer un curseur
        cursor = conn.cursor()
        
        # Exécuter une requête SQL
        cursor.execute("SELECT * FROM etablissement")
        
        # Récupérer tous les résultats
        rows = cursor.fetchall()
        
        # Afficher les résultats
        print("Contenu de la table 'etablissement':")
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Fermer la connexion
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    show_etablissement()
