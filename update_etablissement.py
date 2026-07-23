import sqlite3

def update_etablissement():
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        cursor = conn.cursor()
        
        # Vérifier si la colonne identifiant_fiscal existe, sinon l'ajouter
        cursor.execute("PRAGMA table_info(etablissement)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'identifiant_fiscal' not in columns:
            print("Ajout de la colonne 'identifiant_fiscal' à la table 'etablissement'...")
            cursor.execute("""
                ALTER TABLE etablissement 
                ADD COLUMN identifiant_fiscal TEXT
            """)
            conn.commit()
            print("Colonne 'identifiant_fiscal' ajoutée avec succès.")
        
        # Récupérer les données actuelles
        cursor.execute("SELECT * FROM etablissement LIMIT 1")
        etablissement = cursor.fetchone()
        
        if etablissement:
            print("\nInformations actuelles de l'établissement:")
            print("-" * 50)
            for key in etablissement.keys():
                print(f"{key}: {etablissement[key] if etablissement[key] is not None else 'NULL'}")
            
            # Vérifier si l'identifiant fiscal est déjà défini
            if 'identifiant_fiscal' in etablissement.keys() and etablissement['identifiant_fiscal']:
                print("\nL'identifiant fiscal est déjà défini.")
            else:
                # Si non, demander à l'utilisateur de le saisir
                print("\nL'identifiant fiscal n'est pas encore défini.")
                identifiant = input("Veuillez entrer le numéro d'identifiant fiscal: ").strip()
                
                if identifiant:
                    # Mettre à jour l'identifiant fiscal
                    cursor.execute("""
                        UPDATE etablissement 
                        SET identifiant_fiscal = ?
                        WHERE id = ?
                    """, (identifiant, etablissement['id']))
                    conn.commit()
                    print("\nIdentifiant fiscal mis à jour avec succès!")
                else:
                    print("\nAucun identifiant fiscal saisi. Aucune modification effectuée.")
        else:
            print("Aucun enregistrement trouvé dans la table 'etablissement'.")
            
    except sqlite3.Error as e:
        print(f"\nERREUR SQLite: {e}")
    except Exception as e:
        print(f"\nERREUR: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_etablissement()
