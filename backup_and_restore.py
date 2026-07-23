import sqlite3
import os
from datetime import datetime

def backup_database():
    try:
        # Créer un nom de fichier de sauvegarde avec la date et l'heure actuelles
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data_backup_{timestamp}.db"
        
        # Se connecter à la base de données source
        source = sqlite3.connect('data.db')
        
        # Créer une nouvelle base de données de sauvegarde
        backup = sqlite3.connect(backup_file)
        
        # Sauvegarder la base de données
        source.backup(backup)
        
        print(f"Sauvegarde créée avec succès : {backup_file}")
        
        return backup_file
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return None
    finally:
        if 'source' in locals():
            source.close()
        if 'backup' in locals():
            backup.close()

def restore_database(backup_file):
    try:
        if not os.path.exists(backup_file):
            print(f"Le fichier de sauvegarde {backup_file} n'existe pas.")
            return False
            
        # Renommer le fichier actuel
        if os.path.exists('data.db'):
            os.rename('data.db', 'data_corrupted.db')
            
        # Créer une nouvelle base de données vide
        dest = sqlite3.connect('data.db')
        dest.close()
        
        # Restaurer à partir de la sauvegarde
        backup = sqlite3.connect(backup_file)
        dest = sqlite3.connect('data.db')
        
        backup.backup(dest)
        
        print(f"Base de données restaurée à partir de {backup_file}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la restauration : {e}")
        return False
    finally:
        if 'backup' in locals():
            backup.close()
        if 'dest' in locals():
            dest.close()

if __name__ == "__main__":
    print("1. Créer une sauvegarde")
    print("2. Restaurer à partir d'une sauvegarde")
    choice = input("Choisissez une option (1 ou 2): ")
    
    if choice == '1':
        backup_file = backup_database()
        if backup_file:
            print(f"Sauvegarde réussie dans {backup_file}")
    elif choice == '2':
        backup_file = input("Entrez le nom du fichier de sauvegarde: ")
        if restore_database(backup_file):
            print("Restauration réussie")
    else:
        print("Option invalide")
