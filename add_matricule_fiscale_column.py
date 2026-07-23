import sqlite3

DB_PATH = "data.db"

def ajouter_colonne_matricule_fiscale():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(clients)")
        cols = [r[1] for r in cur.fetchall()]
        if "identifiant_fiscal" not in cols:
            cur.execute("ALTER TABLE clients ADD COLUMN identifiant_fiscal TEXT")
            conn.commit()
            return "La colonne 'identifiant_fiscal' a été ajoutée avec succès."
        return "La colonne 'identifiant_fiscal' existe déjà."
    except Exception as e:
        conn.rollback()
        return f"Erreur lors de l'ajout de la colonne: {e}"
    finally:
        conn.close()

if __name__ == "__main__":
    print(ajouter_colonne_matricule_fiscale())
