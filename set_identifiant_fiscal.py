import sqlite3

def set_identifiant_fiscal(identifiant):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Vérifier si la colonne existe, sinon l'ajouter
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'identifiant_fiscal' not in columns:
            cursor.execute("ALTER TABLE etablissement ADD COLUMN identifiant_fiscal TEXT")
            conn.commit()
        
        # Mettre à jour l'identifiant fiscal
        cursor.execute("UPDATE etablissement SET identifiant_fiscal = ?", (identifiant,))
        conn.commit()
        print(f"Identifiant fiscal mis à jour avec succès: {identifiant}")
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        set_identifiant_fiscal(sys.argv[1])
    else:
        print("Veuillez fournir un identifiant fiscal en argument")
