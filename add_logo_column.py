import sqlite3
import os

def add_logo_column():
    """Ajoute la colonne logo_path à la table etablissement si elle n'existe pas"""
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    
    try:
        # Vérifier si la colonne existe déjà
        cur.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cur.fetchall()]
        
        if 'logo_path' not in columns:
            # Ajouter la colonne logo_path
            cur.execute("""
                ALTER TABLE etablissement 
                ADD COLUMN logo_path TEXT
            """)
            conn.commit()
            print("La colonne 'logo_path' a été ajoutée avec succès.")
        else:
            print("La colonne 'logo_path' existe déjà.")
            
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la colonne: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Créer le dossier pour stocker les logos s'il n'existe pas
    os.makedirs('assets/logos', exist_ok=True)
    add_logo_column()
