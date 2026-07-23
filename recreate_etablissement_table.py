import sqlite3
import os

def recreate_etablissement_table():
    """Recrée la table etablissement avec la structure correcte"""
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    
    try:
        # Supprimer la table si elle existe
        cur.execute("DROP TABLE IF EXISTS etablissement")
        
        # Recréer la table avec la structure correcte
        cur.execute("""
            CREATE TABLE etablissement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                adresse TEXT,
                code_postal TEXT,
                ville TEXT,
                pays TEXT DEFAULT 'Maroc',
                telephone TEXT,
                email TEXT,
                date_creation TEXT
            )
        """)
        
        conn.commit()
        print("La table 'etablissement' a été recréée avec succès.")
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la recréation de la table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    recreate_etablissement_table()
