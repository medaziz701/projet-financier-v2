import sqlite3
import os

def verify_db_structure():
    db_path = 'data.db'
    
    print(f"Vérification de la base de données: {os.path.abspath(db_path)}")
    print(f"Taille du fichier: {os.path.getsize(db_path) / (1024*1024):.2f} Mo")
    
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("\n✓ Connexion à la base de données réussie")
        
        # Vérifier la version de SQLite
        cursor.execute('SELECT sqlite_version()')
        print(f"✓ Version de SQLite: {cursor.fetchone()[0]}")
        
        # Vérifier si la table fournisseurs existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fournisseurs'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("\n✓ La table 'fournisseurs' existe")
            
            # Afficher la structure de la table
            cursor.execute("PRAGMA table_info(fournisseurs)")
            columns = cursor.fetchall()
            print("\nStructure de la table 'fournisseurs':")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
            
            # Compter les fournisseurs
            cursor.execute("SELECT COUNT(*) FROM fournisseurs")
            count = cursor.fetchone()[0]
            print(f"\n✓ Nombre de fournisseurs: {count}")
            
            # Afficher les 5 premiers fournisseurs
            if count > 0:
                print("\nListe des 5 premiers fournisseurs:")
                cursor.execute("SELECT * FROM fournisseurs LIMIT 5")
                for row in cursor.fetchall():
                    print(f"- {row}")
        else:
            print("\n✗ La table 'fournisseurs' n'existe pas dans la base de données")
            
            # Afficher les tables existantes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                print("\nTables disponibles dans la base de données:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("\nAucune table trouvée dans la base de données")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"\n✗ Erreur SQLite: {e}")
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")

if __name__ == "__main__":
    verify_db_structure()
